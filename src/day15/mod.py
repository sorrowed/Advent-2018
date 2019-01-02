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

    @staticmethod
    def is_passable(c):
        return c in [".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def neighbors(self, location, target):

        # Can't move through units. Can move to target
        ul = [unit.location for unit in self.units if unit.location != target]

        n = list()
        # Neighbors are added in reading order to prioritize those paths that have their first position
        # first in reading order *if* there is more than one path to the target
        if location.above() not in ul and Map.is_passable(self[location.above()]):
            n.append(location.above())
        if location.left_of() not in ul and Map.is_passable(self[location.left_of()]):
            n.append(location.left_of())
        if location.right_of() not in ul and Map.is_passable(self[location.right_of()]):
            n.append(location.right_of())
        if location.below() not in ul and Map.is_passable(self[location.below()]):
            n.append(location.below())

        return n

    def targets(self, unit):
        return [u for u in self.units if u.unit_type != unit.unit_type and not u.is_dead()]

    def __str__(self):
        locations = {unit.location: unit for unit in self.units if not unit.is_dead()}

        s = ""
        for y in range(len(self.map)):
            line = self.map[y]
            for x in range(len(line)):
                location = Location(x, y)
                if location in locations:
                    s += locations[location].unit_type
                else:
                    s += line[x]

            s += "\t"

            for unit in sorted([unit for unit in self.units if unit.location.y == y], key=lambda unit: unit.location):
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

            if current == self.target:
                break

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
                # Not storing starting position, but we do store end/target position
                if current != self.start:
                    path.append(current)
                else:
                    break
                current = self.search_map[current]

            path.reverse()
        except KeyError:  # No path exists
            path.clear()

        return path


class Unit:
    def __init__(self, unit_type, x, y):
        self.hp = 200
        self.power = 3
        self.unit_type = unit_type
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
        return "({0}:{1})".format(self.unit_type, self.hp)


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
    map.units.sort(key=lambda unit: unit.location)

    for unit in map.units:

        # Skip if unit died this round before it had a chance to do something
        if unit.is_dead():
            continue

        targets = map.targets(unit)

        # No targets found. Battle ends
        if len(targets) == 0:
            r = False
            break

        # Find any victims to be attacked. If none found find path to nearest target and move
        victim = find_victim(unit, targets)
        if victim is None:
            paths = [path for path in [BreadthFirst(map, unit.location, target.location).path() for target in targets]
                     if len(path) > 0]

            if len(paths) > 0:
                # Shortest path is nearest target. If more of them exist, take the target first in reading order
                # That target is at location path[-1]
                path = sorted(paths, key=lambda path: (len(path), path[-1]))[0]

                # And move....
                unit.move(path[0])

        # Find any victims to be attacked (again, maybe the unit moved into range of a target)
        victim = find_victim(unit, targets)
        if victim is not None:
            unit.attack(victim)

    return r


def battle(map_input, print_steps=False):
    map = Map(map_input)
    print("Start")
    print(map)

    rounds = 0

    while True:
        if not process_round(map):
            print(map)
            print("End")
            break
        else:
            rounds += 1
            if print_steps:
                print(rounds)
                print(map)
            map.reset()

    return rounds, sum([unit.hp for unit in map.units if not unit.is_dead()])


def test():
    map_input = ["#######",
                 "#.G...#",
                 "#...EG#",
                 "#.#.#G#",
                 "#..G#E#",
                 "#.....#",
                 "#######"]
    rounds, hp = battle(map_input)
    assert (rounds * hp == 27730)

    map_input = ["#######",
                 "#G..#E#",
                 "#E#E.E#",
                 "#G.##.#",
                 "#...#E#",
                 "#...E.#",
                 "#######"]
    rounds, hp = battle(map_input)
    assert (rounds * hp == 36334)

    map_input = ["#######",
                 "#E..EG#",
                 "#.#G.E#",
                 "#E.##E#",
                 "#G..#.#",
                 "#..E#.#",
                 "#######"]
    rounds, hp = battle(map_input)
    assert (rounds * hp == 39514)

    map_input = ["#######",
                 "#E.G#.#",
                 "#.#G..#",
                 "#G.#.G#",
                 "#G..#.#",
                 "#...E.#",
                 "#######"]
    rounds, hp = battle(map_input)
    assert (rounds * hp == 27755)

    map_input = ["#######",
                 "#.E...#",
                 "#.#..G#",
                 "#.###.#",
                 "#E#G#G#",
                 "#...#G#",
                 "#######"]
    rounds, hp = battle(map_input)
    assert (rounds * hp == 28944)

    map_input = ["#########",
                 "#G......#",
                 "#.E.#...#",
                 "#..##..G#",
                 "#...##..#",
                 "#...#...#",
                 "#.G...G.#",
                 "#.....G.#",
                 "#########"]
    rounds, hp = battle(map_input)
    assert (rounds * hp == 18740)


def first():
    return battle(INPUT, True)


def second():
    return 0


if __name__ == "__main__":
    test()

    rounds, hp = first()
    print("Battled for {0} rounds and left with {1} HP for a total of {2}".format(rounds, hp, rounds * hp))
    #
    # print("Blaat: {0}".format(second()))
