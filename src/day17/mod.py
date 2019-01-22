import re

pattern = re.compile(r"(\w)=(\d*),.*(\w)=(\d*)\.\.(\d*)")


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

    def left(self):
        return Location(self.x - 1, self.y)

    def right(self):
        return Location(self.x + 1, self.y)

    def down(self):
        return Location(self.x, self.y + 1)

    @staticmethod
    def copy(loc):
        return Location(loc.x, loc.y)


class Square:
    id = 0

    def __init__(self, loc, fill):
        self.loc = loc
        self.from_loc = None
        self.fill = fill
        self.has_flowed = False

    def __str__(self):
        return "{0}:{1}".format(str(self.loc), self.fill)

    def is_clay(self):
        return self.fill == '#'

    def is_water(self):
        return self.fill == '~'

    def is_dried(self):
        return self.fill == '|'

    def is_sand(self):
        return self.fill == '.' or self.is_dried();

    @staticmethod
    def sand(loc):
        return Square(loc, ".")

    @staticmethod
    def clay(loc):
        return Square(loc, "#")

    @staticmethod
    def well(loc):
        return Square(loc, "+")

    @staticmethod
    def water(loc):
        return Square(loc, "~")

    @staticmethod
    def dried(loc):
        return Square(loc, "|")


class Map:
    def __init__(self, tl, br):
        self.tl = tl
        self.br = br

        m = list()
        for y in range(self.height()):
            m.append([Square.sand(Location(tl.x + x, tl.y + y)) for x in range(self.width())])
        self.map = m

    def width(self):
        return 1 + self.br.x - self.tl.x

    def height(self):
        return 1 + self.br.y - self.tl.y

    def __getitem__(self, loc):
        return self.map[loc.y - self.tl.y][loc.x - self.tl.x]

    def __setitem__(self, loc, value):
        self.map[loc.y - self.tl.y][loc.x - self.tl.x] = value

    def __str__(self):
        s = str()
        for row in self.map:
            s += "".join([s.fill for s in row]) + "\n"

        return s

    def is_valid(self, loc):
        return self.tl.x <= loc.x <= self.br.x and \
               self.tl.y <= loc.y <= self.br.y

    def flow(self, locations):

        loc = locations.pop()

        # flow down
        while self.is_valid(loc.down()) and self[loc.down()].is_sand():
            self[loc] = Square.dried(loc)
            loc = loc.down()

        if not self.is_valid(loc.down()):
            self[loc] = Square.dried(loc)
            return False

        hp = Location.copy(loc)
        spilled = False

        # flow left (from hp)
        while not self[loc].is_clay():
            self[loc] = Square.water(loc)

            d = loc.down()
            if self[d].is_sand():
                locations.append(d)
                spilled = True
                break

            loc = loc.left()

        # flow right (from hp)
        loc = Location.copy(hp)
        while not self[loc].is_clay():
            self[loc] = Square.water(loc)
            d = loc.down()
            if self[d].is_sand():
                locations.append(d)
                spilled = True
                break
            loc = loc.right()

        # Dry hp row if spilled left and/or right
        if spilled:
            loc = Location.copy(hp)
            while self[loc].is_water():
                self[loc] = Square.dried(loc)
                loc = loc.left()
            loc = hp.right()  # because hp was already dried
            while self[loc].is_water():
                self[loc] = Square.dried(loc)
                loc = loc.right()

        return not spilled

    def dried_or_water_squares(self):
        return sum(len([s for s in row if s.is_water() or s.is_dried()]) for row in self.map)

    def water_squares(self):
        return sum(len([s for s in row if s.is_water()]) for row in self.map)


def get_input():
    with open("input.txt", "r") as f:
        return f.readlines()


def parse_squares(line):
    matches = pattern.match(line)

    if line.startswith('x'):
        x_range = range(int(matches.group(2)), int(matches.group(2)) + 1)
        y_range = range(int(matches.group(4)), int(matches.group(5)) + 1)
    elif line.startswith('y'):
        y_range = range(int(matches.group(2)), int(matches.group(2)) + 1)
        x_range = range(int(matches.group(4)), int(matches.group(5)) + 1)

    return [Square.clay(Location(x, y)) for y in y_range for x in x_range]


def squares_find_extends(squares):
    left, top = min([s.loc.x for s in squares]), min([s.loc.y for s in squares])
    right, bottom = max([s.loc.x for s in squares]), max([s.loc.y for s in squares])

    return Location(left, top), Location(right, bottom)


def create_map(inp):
    squares = list()
    for line in inp:
        squares.extend(parse_squares(line))

    tl, br = squares_find_extends(squares)

    # Extend to left and right so water may flow left and right freely
    tl.x -= 1
    br.x += 1

    map = Map(tl, br)
    for square in squares:
        map[square.loc] = square

    return map


def flow(inp):
    map = create_map(inp)
    locations = list()

    for _ in range(20000):
        if len(locations) == 0:
            water = Square.water(Location(500, map.tl.y))
            map[water.loc] = water
            locations.append(water.loc)

        map.flow(locations)

    return map


def test():
    inp = ["x=495, y=2..7",
           "y=7, x=495..501",
           "x=501, y=3..7",
           "x=498, y=2..4",
           "x=506, y=1..2",
           "x=498, y=10..13",
           "x=504, y=10..13",
           "y=13, x=498..504"]

    map = flow(inp)

    print(map)
    return map.dried_or_water_squares()


def first(map):
    print(map)

    return map.dried_or_water_squares()


def second(map):
    return map.water_squares()


if __name__ == "__main__":
    print("Number of tiles the water can reach on the test map: {0}".format(test()))

    map = flow(get_input())

    print("Number of tiles the water can reach: {0}".format(first(map)))
    print("Number of tiles that holds water: {0}".format(second(map)))
