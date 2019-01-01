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
        for y in range(len(self.map)):
            line = self.map[y]
            for x in range(len(line)):
                if line[x] != '#' and line[x] != '.':
                    line[x] = '.'

    @staticmethod
    def process(source_map):
        m, units = list(), list()

        for y in range(len(source_map)):
            line = list()
            for x in range(len(source_map[y])):

                c = source_map[y][x]

                if c == "G" or c == "E":
                    units.append(Unit(c, x, y))
                    line.append(".")  # Make sure locations with units are normally passable
                else:
                    line.append(c)

            m.append(line)

        return m, units

    def neighbors(self, location, target):
        # Can't move through units. Can move to target
        ul = [unit.location for unit in self.units if unit.location != target]

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

    def targets(self, unit):
        return [u for u in self.units if u.type != unit.type and not u.is_dead()]

    def __str__(self):
        locations = {unit.location: unit for unit in self.units if not unit.is_dead()}

        s = ""
        for y in range(len(self.map)):
            line = self.map[y]
            for x in range(len(line)):
                location = Location(x, y)
                if location in locations:
                    s += locations[location].type
                else:
                    s += line[x]

            s += "\t"

            for unit in self.units:
                if unit.location.y == y:
                    s += str(unit)

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

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)


class BreadthFirst:
    def __init__(self, map, start, target):
        self.start = start
        self.target = target
        self.search_map = self.calculate_path_map(map)

    def calculate_path_map(self, map):
        frontier = queue.Queue()
        frontier.put(self.start)

        path_map = dict()
        path_map[self.start] = None

        while not frontier.empty():
            current = frontier.get()

            for n in map.neighbors(current, self.target):
                if n not in path_map:
                    frontier.put(n)
                    path_map[n] = current

        return path_map

    def path(self):
        """
        Find path to nearest location next to target (either above/below/left of or right of)
        """
        current = self.target

        path = list()
        try:
            while True:
                # Not storing first current(==target) because we need to move beside the target, not on it
                current = self.search_map[current]

                # Not storing starting position either
                if current != self.start:
                    path.append(current)
                else:
                    break

            path.reverse()
        except KeyError:  # No path exists
            path.clear()

        return path


class Unit:
    def __init__(self, type, x, y):
        self.hp = 200
        self.power = 3
        self.type = type
        self.location = Location(x, y)

    def distance(self, other):
        return abs(other.location.x - self.location.x) + abs(other.location.y - self.location.y)

    def move(self, location):
        self.location = location

    def attack(self, unit):
        if not unit.is_dead():
            unit.hp -= min(self.power, unit.hp)

    def is_dead(self):
        return self.hp <= 0

    def __str__(self):
        return "({0}:{1})".format(self.type, self.hp)


def find_victim(src, targets):
    # Get all non-dead targets in attack range
    victims = [target for target in targets if not target.is_dead() and src.distance(target) <= 1]

    # Sort target by smallest HP, then reading order based on location
    victims.sort(key=lambda u: (u.hp, u.location))

    return victims[0] if len(victims) > 0 else None


def process_round(map):
    r = True

    # Remove dead units
    map.units = [unit for unit in map.units if not unit.is_dead()]

    # Sort units in reading order based on location
    map.units.sort(key=lambda u: u.location)

    for u in map.units:
        print(u)
        
    for unit in map.units:

        if unit.is_dead():
            continue

        targets = map.targets(unit)

        if len(targets) == 0:
            r = False
            break

        victim = find_victim(unit, targets)
        if victim is not None:
            unit.attack(victim)
        else:
            paths = [BreadthFirst(map, unit.location, target.location).path() for target in
                     targets]

            # Filter empty paths.
            nearest_path = [path for path in paths if len(path) > 0]
            # Shortest path is nearest target. If more of them exist, take the target first in reading order
            nearest_path.sort(key=lambda p: (len(p), p[0]))

            if len(nearest_path) > 0:
                unit.move(nearest_path[0][0])

    return r


def test():
    map_input = ["#######",
                 "#.G...#",
                 "#...EG#",
                 "#.#.#G#",
                 "#..G#E#",
                 "#.....#",
                 "#######"]

    map = Map(map_input)
    print(map)

    battle = True
    rounds = 0

    while battle:
        if not process_round(map):
            rounds -= 1  # Last target died in previous round
            print(map)
            break
        else:
            rounds += 1
            print(rounds)
            print(map)

    return rounds, sum([unit.hp for unit in map.units if not unit.is_dead()])


def first():
    return 0


def second():
    return 0


if __name__ == "__main__":
    t = test()
    print(t[0], t[1])

    print("Blaat: {0}".format(first()))
    print("Blaat: {0}".format(second()))
