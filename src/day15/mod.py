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

    def process(self, source_map):
        m, units = list(), list()

        for y in range(len(source_map)):
            line = list()
            for x in range(len(source_map[y])):
                if source_map[y][x] == "#" or source_map[y][x] == ".":
                    line.append(source_map[y][x])
                elif source_map[y][x] == "G" or source_map[y][x] == "E":
                    units.append(Unit(source_map[y][x], x, y))
                    line.append(".")

            m.append(line)

        return m, units

    def neighbors(self, location):
        n = list()
        if self[location.above()] != "#":
            n.append(location.above())
        if self[location.right_of()] != "#":
            n.append(location.right_of())
        if self[location.below()] != "#":
            n.append(location.below())
        if self[location.left_of()] != "#":
            n.append(location.left_of())

        return n

    def __str__(self):
        s = ""
        for y in range(len(self.map)):
            s += str(self.map[y]) + "\n"
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

    def __hash__(self):
        return hash((self.y << 16) | self.x)


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

    def path(self, target):
        current = target

        path = []
        while current != self.start:
            path.append(current)
            current = self.search_map[current]
        #path.append(self.start)
        path.reverse()  # optional

        return path


class Unit:
    def __init__(self, type, x, y):
        self.hp = 200
        self.type = type
        self.location = Location(x, y)


def test():
    map = Map(INPUT)
    print(map)

    src = map.units[0]
    target = map.units[1]

    bf = BreadthFirst(map, src.location)

    path = bf.path(target.location)

    n = 1
    for location in path:
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
