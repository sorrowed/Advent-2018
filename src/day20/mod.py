import queue


def get_input():
    with open("input.txt", "r") as f:
        return f.read()


class BreadthFirst:
    def __init__(self, map, start):
        self.start = start
        self.path_map = self.calculate_path_map(map)

    def calculate_path_map(self, map):
        frontier = queue.Queue()
        frontier.put(self.start)

        path_map = dict()
        path_map[self.start] = None

        while not frontier.empty():
            current = frontier.get()

            for n in map.neighbors(current):
                if n not in path_map:
                    frontier.put(n)
                    path_map[n] = current

        return path_map

    def path(self, target):
        """
        Find path to target
        """
        current = target

        path = list()
        try:
            while True:
                current = self.path_map[current]

                # Not storing start and target position
                if current == self.start:
                    break

                path.append(current)

            path.reverse()

        except KeyError:  # No path exists
            path.clear()

        return path


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


class Map:
    def __init__(self):
        self.map = dict()
        self.markers = list()

    def __getitem__(self, location):
        try:
            return self.map[(location.x, location.y)]
        except KeyError:
            return "#"

    def __setitem__(self, location, v):
        self.map[(location.x, location.y)] = v

    def limits(self):
        x_min = min(self.map.keys(), key=lambda k: k[0])[0]
        y_min = min(self.map.keys(), key=lambda k: k[1])[1]
        x_max = max(self.map.keys(), key=lambda k: k[0])[0]
        y_max = max(self.map.keys(), key=lambda k: k[1])[1]

        return Location(x_min, y_min), Location(x_max, y_max)

    def __str__(self):
        tl, br = self.limits()
        de = self.dead_ends()

        s = str()
        for y in range(tl.y - 1, br.y + 2):  # Add border
            line = ""
            for x in range(tl.x - 1, br.x + 2):

                location = Location(x, y)

                if location in de:
                    line += "@"
                elif location in self.markers:
                    line += "*"
                else:
                    line += self[location]

            s += line + "\n"

        return s

    def start(self, location):
        self[location] = 'X'

    def add_markers(self, l):
        self.markers.extend(l)

    @staticmethod
    def is_start(c):
        return c == "X"

    @staticmethod
    def is_room(c):
        return c == "." or Map.is_start(c)

    @staticmethod
    def is_door(c):
        return c == "|" or c == "-"

    def dead_ends(self):
        """
        Find all dead ends: All rooms with only one door neighbour
        """
        n = list()

        for (x, y) in self.map:

            location = Location(x, y)
            c = self[location]
            if Map.is_start(c) or (not Map.is_room(c)):
                continue

            if len(self.neighbor_doors(location)) == 1:
                n.append(location)

        return n

    def neighbor_doors(self, location):
        """
        Returns all neighbor doors for location
        """
        n = [location.above(), location.right_of(), location.below(), location.left_of()]

        return [l for l in n if Map.is_door(self[l])]

    def neighbor_rooms(self, location):
        """
        Returns all neighbor rooms for location
        """
        n = [location.above(), location.right_of(), location.below(), location.left_of()]

        return [l for l in n if Map.is_room(self[l])]

    def neighbors(self, location):
        return self.neighbor_doors(location) if \
            Map.is_room(self[location]) else self.neighbor_rooms(location)


class Path:
    def __init__(self, location):
        self.current = location

    def step(self, c, m):

        current = self.current

        if c == "E":
            current.x += 1
            m[current] = "|"
            current.x += 1
        elif c == "N":
            current.y -= 1
            m[current] = "-"
            current.y -= 1
        elif c == "W":
            current.x -= 1
            m[current] = "|"
            current.x -= 1
        elif c == "S":
            current.y += 1
            m[current] = "-"
            current.y += 1

        m[current] = "."


def traverse(inp, m):
    stack = list()  # Path stack

    p = Path(Location(0, 0))

    for c in inp:
        if c == "^":
            pass
        elif c == "(":  # Start of path group, push parent on stack
            child = Path(Location.copy(p.current))
            stack.append(p)
            p = child
        elif c == "|":  # End of child path. Continue with another child path in group, use same parent
            p = stack.pop()
            child = Path(Location.copy(p.current))
            stack.append(p)
            p = child
        elif c == ")" or c == "$":  # End of path group. Pop parent (if any) from stack. (This might discard an empty child path)
            if len(stack) > 0:
                p = stack.pop()
        else:
            p.step(c, m)  # Add step to current path


def test():
    inp = [r"^WNE$", r"^ENWWW(NEEE|SSE(EE|N))$", r"^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$",
           r"^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))",
           r"^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"]

    for i in inp:
        m = Map()
        m.start(Location(0, 0))

        traverse(iter(i), m)

        bf = BreadthFirst(m, Location(0, 0))

        # Find paths from start position to all dead ends
        paths = [bf.path(de) for de in m.dead_ends()]

        # Find the longest path, and only remember the doors (starts at first position with one room in between)
        doors = max(paths, key=lambda path: len(path))[0::2]

        m.add_markers(doors)

        print(m, len(doors))


def first():
    # Construct the map and BF search map
    m = Map()
    m.start(Location(0, 0))

    traverse(get_input(), m)

    bf = BreadthFirst(m, Location(0, 0))

    # Find paths from start position to all dead ends
    paths = [bf.path(de) for de in m.dead_ends()]

    # Find the longest path, remember doors only (first door is at first position, one room in between doors)
    doors = max(paths, key=lambda path: len(path))[0::2]

    m.add_markers(doors)

    print(m, len(doors))

    return len(doors)


def second():
    # Construct the map and BF search map
    m = Map()
    m.start(Location(0, 0))

    traverse(get_input(), m)

    bf = BreadthFirst(m, Location(0, 0))

    # Generate all rooms (make sure to exclude start room because that path is empty)
    rooms = (Location(r[0], r[1]) for r in m.map if
             not Map.is_start(m[Location(r[0], r[1])]) and Map.is_room(m[Location(r[0], r[1])]))

    # Find paths from start to all rooms and select those with 1000 or more doors
    paths = [p for p in (bf.path(r)[0::2] for r in rooms) if len(p) >= 1000]

    print(len(paths))
    return len(paths)


if __name__ == "__main__":
    test()
    print("Number of doors to furthest room: {0}".format(first()))
    print("Number of paths with at least 1000 doors: {0}".format(second()))
