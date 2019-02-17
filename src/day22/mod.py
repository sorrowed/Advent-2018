import queue

TYPE_ROCKY = 0
TYPE_WET = 1
TYPE_NARROW = 2

ITEM_NEITHER = 0
ITEM_TORCH = 1
ITEM_GEAR = 2

DEPTH = 11817
TARGET = (9, 751)


class GeoLogicIndexError(Exception):
    pass


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def above(self):
        return Location(self.x, self.y - 1)

    def left_of(self):
        return Location(self.x - 1, self.y)

    def right_of(self):
        return Location(self.x + 1, self.y)

    def below(self):
        return Location(self.x, self.y + 1)

    def tuple(self):
        return self.x, self.y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return hash(self) < hash(other)

    def __hash__(self):
        return hash((self.y << 16) | self.x)

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

    @staticmethod
    def copy(location):
        return Location(location.x, location.y)


def geologic_index_normal(location, target):
    return location == Location(0, 0) or location == target or location.x == 0 or location.y == 0


def geologic_index(location, target):
    """
    The region at 0,0 (the mouth of the cave) has a geologic index of 0.
    The region at the coordinates of the target has a geologic index of 0.
    If the region's Y coordinate is 0, the geologic index is its X coordinate times 16807.
    If the region's X coordinate is 0, the geologic index is its Y coordinate times 48271.
    """

    if not geologic_index_normal(location, target):
        raise GeoLogicIndexError()

    gi = None
    if location == Location(0, 0) or location == target:
        gi = 0
    elif location.y == 0:
        gi = location.x * 16807
    elif location.x == 0:
        gi = location.y * 48271

    return gi


def erosion_level(location, target, depth):
    """
        A region's erosion level is its geologic index plus the cave system's depth, all modulo 20183
    """
    return (depth + geologic_index(location, target)) % 20183


def region_type(el):
    """
    If the erosion level modulo 3 is 0, the region's type is rocky.
    If the erosion level modulo 3 is 1, the region's type is wet.
    If the erosion level modulo 3 is 2, the region's type is narrow.
    """
    return el % 3


class ErosionLevelMap:
    def __init__(self, size, target, depth):
        self.size = size
        self.target = target
        self.depth = depth
        self.map = self.build_map()
        self.path = None

    def build_map(self):
        m = dict()
        for y in range(0, self.size.y + 1):
            for x in range(0, self.size.x + 1):
                location = Location(x, y)

                if not geologic_index_normal(location, self.target):
                    # Otherwise, the region's geologic index is the result of
                    # multiplying the erosion levels of the regions at X-1,Y and X,Y-1.
                    m[(x, y)] = (self.depth + (m[location.left_of().tuple()] * m[location.above().tuple()])) % 20183
                else:
                    m[(x, y)] = erosion_level(location, self.target, self.depth)

        return m

    def __getitem__(self, location):
        return self.map[location.tuple()]

    def risk_level(self):
        return sum([region_type(l) for l in self.map.values()])

    def __str__(self):
        s = str()
        for y in range(0, self.size.y + 1):
            for x in range(0, self.size.x + 1):
                rt = region_type(self[Location(x, y)])

                if rt == TYPE_ROCKY:
                    s += "."
                elif rt == TYPE_WET:
                    s += "="
                elif rt == TYPE_NARROW:
                    s += "|"
                else:
                    s += "?"

            s += "\n"

        return s


class CavernLocation:
    def __init__(self, location, item):
        self.location = location
        self.item = item

    def key(self):
        return self.location.x, self.location.y, self.item

    def neighbors(self, el_map):
        """
        Determine possible target CavernLocations (states) from this location
        """
        neighbors = self.make_neighbors(el_map.size)

        return [CavernLocation(n, item) for n in neighbors for item in self.items(el_map, n)]

    def make_neighbors(self, br):
        n = list()
        if self.location.x > 0:
            n.append(self.location.left_of())
        if self.location.y > 0:
            n.append(self.location.above())

        if self.location.x < br.x:
            n.append(self.location.right_of())

        if self.location.y < br.y:
            n.append(self.location.below())

        return n

    def __str__(self):
        item = "-" if self.item == ITEM_NEITHER else \
            "T" if self.item == ITEM_TORCH else \
                "G" if self.item == ITEM_GEAR else "?"

        return "({},{},{})".format(self.location.x, self.location.y, item)

    def __lt__(self, other):
        return self.location < other.location and self.item < other.item

    @staticmethod
    def items(el_map, target):
        rt = region_type(el_map[target])

        o = None
        if rt == TYPE_ROCKY:
            o = [ITEM_TORCH, ITEM_GEAR]
        elif rt == TYPE_WET:
            o = [ITEM_NEITHER, ITEM_GEAR]
        elif rt == TYPE_NARROW:
            o = [ITEM_NEITHER, ITEM_TORCH]

        return o

    @staticmethod
    def cost(source, target):

        """
        Determine the cost/time to move from this location to target
        """
        return 1 if target.item == source.item else 8


class Path:
    def __init__(self, start):
        self.steps = [start]
        self.cost = 0

    def add(self, step, cost):
        print("Adding {0} with cost {1}".format(step, cost))

        self.cost += cost
        self.steps.append(step)

    def complete(self):
        self.steps.reverse()

    def clear(self):
        self.steps.clear()
        self.cost = 0

    def __str__(self):
        s = str(self.steps[0])
        for step in self.steps[1:]:
            s += " -> {0}".format(step)
        return s


class Dijkstra:
    def __init__(self, start, el_map):
        print(el_map.target)

        self.start = start
        self.path_map = self.calculate_path_map(el_map)

    def calculate_path_map(self, el_map):
        frontier = queue.PriorityQueue()
        frontier.put((0, self.start))

        path_map = dict()
        path_map[self.start.key()] = None

        cost_so_far = dict()
        cost_so_far[self.start.key()] = 0

        while not frontier.empty():
            current = frontier.get()[1]

            for n in current.neighbors(el_map):

                cost = cost_so_far[current.key()] + CavernLocation.cost(current, n)

                if n.key() not in cost_so_far or cost < cost_so_far[n.key()]:
                    cost_so_far[n.key()] = cost
                    frontier.put((cost, n))
                    path_map[n.key()] = current

        return path_map

    def path(self, target):
        """
        Find path to target
        """
        current = target

        path = Path(current)

        try:
            while current != self.start:
                nx = self.path_map[current.key()]

                path.add(nx, CavernLocation.cost(current, nx))

                current = nx

            path.complete()

        except KeyError:  # No path exists
            path.clear()

        return path


def test():
    depth = 510
    target = Location(10, 10)

    el_map = ErosionLevelMap(target, target, depth)

    assert region_type(el_map[Location(0, 0)]) == TYPE_ROCKY
    assert region_type(el_map[Location(1, 0)]) == TYPE_WET
    assert region_type(el_map[Location(0, 1)]) == TYPE_ROCKY
    assert region_type(el_map[Location(1, 1)]) == TYPE_NARROW
    assert region_type(el_map[target]) == TYPE_ROCKY

    print(el_map, el_map.risk_level())

    assert el_map.risk_level() == 114


def first():
    target = Location(*TARGET)

    el_map = ErosionLevelMap(target, target, DEPTH)

    return el_map.risk_level()


def second():
    depth = 510
    target = Location(10, 10)
    size = Location(target.x + 6, target.y + 6)

    el_map = ErosionLevelMap(size, target, depth)
    print(el_map)

    mouth = CavernLocation(Location(0, 0), ITEM_TORCH)

    dijkstra = Dijkstra(mouth, el_map)

    target = CavernLocation(target, ITEM_TORCH)

    path = dijkstra.path(target)

    print(path)

    return path.cost


if __name__ == "__main__":
    test()
    print("Risk level of {0}: {1}".format(Location(10, 10), first()))
    print("Bleerp: {0}".format(second()))
