import re
import sys

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
        return self.fill in ['~', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

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
        Square.id = (Square.id + 1) % 10
        return Square(loc, str(Square.id))

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

    def flow(self, loc):
        while self.is_valid(loc.down()) and self[loc.down()].is_sand():
            self[loc] = Square.dried(loc)
            loc = loc.down()
        self[loc] = Square.water(loc)

        locations = list()

        l = Location.copy(loc).left()
        while self[l].is_sand():
            self[l] = Square.water(l)

            if not self.is_valid(l.down()) or self[l.down()].is_sand():

                if self.is_valid(l.down()) and self[l.down()].is_sand():
                    locations.append(l)

                while self[l].is_water() or self[l].is_dried():
                    self[l] = Square.dried(l)
                    l = l.right()
                break

            l = l.left()

        l = Location.copy(loc).right()
        while self[l].is_sand():
            self[l] = Square.water(l)

            if not self.is_valid(l.down()) or self[l.down()].is_sand():
                if self.is_valid(l.down()) and self[l.down()].is_sand():
                    locations.append(l)
                while self[l].is_water() or self[l].is_dried():
                    self[l] = Square.dried(l)
                    l = l.left()
                break
            l = l.right()

        for loc in locations:
            self.flow(loc)


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

    return Location(left - 1, top), Location(right + 1, bottom)


def create_map(inp):
    squares = list()
    for line in inp:
        squares.extend(parse_squares(line))
    squares.append(Square.well(Location(500, 0)))

    tl, br = squares_find_extends(squares)

    map = Map(tl, br)
    for square in squares:
        map[square.loc] = square

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

    map = create_map(inp)
    water = Square.water(Location(500, 1))
    for _ in range(100):
        map[water.loc] = water
        map.flow(water.loc)
    print(map)


def first():
    map = create_map(get_input())
    water = Square.water(Location(500, 1))
    for _ in range(100):
        map[water.loc] = water
        map.flow(water.loc)
    print(map)

    return map.water_squares()


def second():
    pass


if __name__ == "__main__":
    test()
    print("Number of tiles the water can reach: {0}".format(first()))
# print("Some other graph questions answer: {0}".format(second()))
