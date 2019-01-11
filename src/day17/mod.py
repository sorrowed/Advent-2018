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

    def can_flow_to(self):
        return not self.is_water() and not self.is_clay()

    def is_clay(self):
        return self.fill == '#'

    def is_water(self):
        return self.fill in ['~', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

    def was_water(self):
        return self.fill == '|'

    def is_well(self):
        return self.fill == '+'

    def came_from(self, loc):
        return self.from_loc is not None and loc.x == self.from_loc.x and loc.y == self.from_loc.y

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

    def apply_region(self, region):
        for square in region.squares:
            self[square.loc] = square

    def move_to(self, to_square, from_square):

        if to_square is not None:
            target = Square(Location.copy(to_square.loc), from_square.fill)
            target.from_loc = Location.copy(from_square.loc)
            target.has_flowed = True
            self[to_square.loc] = target

        self[from_square.loc] = Square.dried(Location.copy(from_square.loc))

    def flow(self):
        equilibrium = True
        # Iterate from bottom to top

        for l in self.map:
            for s in l:
                s.has_flowed = False

        for y in range(self.br.y, self.tl.y - 1, -1):

            # Iterate from leftmost column to rightmost column
            # fixme: this should iterate from outside to inside to make sure that
            # water that has moved also causes other water that was previously blocked to move
            for x in range(self.tl.x, self.br.x + 1):
                loc = Location(x, y)

                current = self[loc]

                if not current.has_flowed and current.is_water():
                    left = self[loc.left()] if x > 0 else None
                    right = self[loc.right()] if x < self.br.x else None
                    below = self[loc.down()] if y < self.br.y else None

                    if below is None or (below.can_flow_to() and not current.came_from(below.loc)):
                        equilibrium = False
                        self.move_to(below, current)

                    elif left is None or (left.can_flow_to() and not current.came_from(left.loc)):
                        equilibrium = False
                        self.move_to(left, current)

                    elif right is None or (right.can_flow_to() and not current.came_from(right.loc)):
                        equilibrium = False
                        self.move_to(right, current)

        return equilibrium


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
    print(map)

    for _ in range(19):
        water = Square.water(Location(500, 1))
        map[water.loc] = water
        map.flow()
        print(map)
        raw_input()

    while not map.flow():
        print(map)
        raw_input()


def first():
    map = create_map(get_input())
    print(map)


def second():
    pass


if __name__ == "__main__":
    test()
    # print("Number of tiles the water can reach: {0}".format(first()))
    # print("Some other graph questions answer: {0}".format(second()))
