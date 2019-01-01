import queue

INPUT = ["################################",
         "#####################...########",
         "###################....G########",
         "###################....#########",
         "#######.##########......########",
         "#######G#########........#######",
         "#######G#######.G.........######",
         "#######.######..G.........######",
         "#######.......##.G...G.G..######",
         "########..##..#....G......G#####",
         "############...#.....G.....#####",
         "#...#######..........G.#...#####",
         "#...#######...#####G......######",
         "##...######..#######G.....#.##.#",
         "###.G.#####.#########G.........#",
         "###G..#####.#########.......#.E#",
         "###..######.#########..........#",
         "###.......#.#########.....E..E.#",
         "#####G...#..#########.......#..#",
         "####.G.#.#...#######.....G.....#",
         "########......#####...........##",
         "###########..................###",
         "##########.................#####",
         "##########.................#####",
         "############..E.........E.....##",
         "############.........E........##",
         "###############.#............E##",
         "##################...E..E..##.##",
         "####################.#E..####.##",
         "################.....######...##",
         "#################.#..###########",
         "################################"]


class Map:
    def __init__(self, source_map):
        self.map, self.units = self.process(source_map)

    def __getitem__(self, location):
        return self.map[location.y][location.x]

    def __setitem__(self, location, value):
        self.map[location.y][location.x] = value

    def reset(self):
        pass

    @staticmethod
    def process(source_map):
        m, units = list(), list()

        for y in range(len(source_map)):
            line = list()
            for x in range(len(source_map[y])):

                c = source_map[y][x]

                if c == "G" or c == "E":
                    units.append(Unit(c, x, y))
                    line.append(".")
                else:
                    line.append(c)

            m.append(line)

        return m, units

    def neighbors(self, location):
        # Can't move through units
        ul = [unit.location for unit in self.units]

        n = list()
        if location.above() not in ul and self[location.above()] == ".":
            n.append(location.above())
        if location.right_of() not in ul and self[location.right_of()] == ".":
            n.append(location.right_of())
        if location.below() not in ul and self[location.below()] == ".":
            n.append(location.below())
        if location.left_of() not in ul and self[location.left_of()] == ".":
            n.append(location.left_of())

        return n

    def __str__(self):
        locations = {unit.location: unit for unit in self.units}

        s = ""
        for y in range(len(self.map)):
            line = self.map[y]
            for x in range(len(line)):
                location = Location(x, y)
                if location in locations:
                    s += locations[location].type
                else:
                    s += line[x]

            s += "\n"

        return s


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


def manhattan_distance(a, b):
    return abs(b.x - a.x) + abs(b.y - a.y)


class BreadthFirst:
    def __init__(self, map, start):
        self.start = start
        self.search_map = self.calculate_path_map(map, start)

    @staticmethod
    def calculate_path_map(map, start, target=None):
        frontier = queue.Queue()
        frontier.put(start)

        path_map = dict()
        path_map[start] = None

        while not frontier.empty():
            current = frontier.get()

            # Bail out early if target (if any) was found
            if target is not None and current == target:
                break

            for n in map.neighbors(current):

                if n not in path_map:
                    frontier.put(n)
                    path_map[n] = current

        return path_map

    def path_near(self, target):
        """
        Find path to nearest location next to target (either above/below/left of or right of)
        """
        current = target

        path = list()
        try:
            while manhattan_distance(current, self.start) >= 1:
                path.append(current)
                current = self.search_map[current]

            path.reverse()
        except KeyError:  # No path exists
            path.clear()

        return path


class Unit:
    def __init__(self, type, x, y):
        self.hp = 200
        self.type = type
        self.location = Location(x, y)


def test():
    map = Map(INPUT)
    print(map)

    # Sort units in top-down/left-right fashion (reading order) based on location
    map.units.sort(key=lambda u: u.location)

    src = map.units[0]

    bf = BreadthFirst(map, src.location)

    targets = [u for u in map.units if u.type != src.type]
    targets = [map.units[2]]
    paths = [bf.path_near(target.location) for target in targets]

    # Filter empty paths.
    nearest_path = [path for path in paths if len(path) > 0]
    # Shortest path is nearest target. If more of them exist, take the target first in reading order
    nearest_path.sort(key=lambda p: (len(p), p[0]))

    n = 1
    for location in nearest_path[0]:
        map[location] = str(n % 10)
        n += 1

    print(map)


def first():
    return 0


def second():
    return 0


if __name__ == "__main__":
    test()
    print("Blaat: {0}".format(first()))
    print("Blaat: {0}".format(second()))
