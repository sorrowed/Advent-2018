def get_input():
    with open("input.txt", "r") as f:
        return f.readlines()


def get_collisions(carts):
    r = list()
    for cart in carts:
        if not cart.broken:
            r.extend(
                [c for c in carts if
                 c is not cart and c.location.x == cart.location.x and c.location.y == cart.location.y and not c.broken])
    return r


class Location:
    def __init__(self, x, y):
        self.y = y
        self.x = x

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)

    def __lt__(self, other):
        """Make Location top-down, left-right sortable"""
        return self.y < other.y or self.x < other.x


class Map:
    orientations = ["^", ">", "v", "<"]

    def __init__(self, lines):
        self.lines = [line.replace("\n", "") for line in lines]
        self.carts = list()

    def __getitem__(self, location):
        return self.lines[location.y][location.x]

    def print(self):
        for y in range(len(self.lines)):
            line = self.lines[y]
            s = ""
            for x in range(len(line)):
                carts = [c for c in self.carts if c.location.x == x and c.location.y == y]
                if len(carts) == 0:
                    s += self[Location(x, y)]
                elif len(carts) == 1:
                    s += carts[0].o
                else:
                    s += "X"
            print(s)

    def prepare(self):
        for y in range(len(self.lines)):
            line = self.lines[y]
            for x in range(len(line)):

                location = Location(x, y)

                c = self[location]

                if c in Map.orientations:
                    self.carts.append(Cart(location, c))

        for l in range(len(self.lines)):
            self.lines[l] = self.lines[l].replace(">", "-").replace("<", "-").replace("^", "|").replace("v", "|")


class Cart:

    def __init__(self, location, o):
        self.location = location
        self.o = o
        self.last = None
        self.broken = False
        self.id = (location.x, location.y)

    def move(self, map):
        if self.o == "^":
            self.location.y -= 1
        elif self.o == ">":
            self.location.x += 1
        elif self.o == "v":
            self.location.y += 1
        elif self.o == "<":
            self.location.x -= 1

        c = map[self.location]

        self.orientation(c)

        # print((self.location.x, self.location.y), c, self.o)

    def orientation(self, c):

        if c == "/":
            if self.o == "^" or self.o == "v":
                self.turn_right()
            elif self.o == ">" or self.o == "<":
                self.turn_left()
        elif c == "\\":
            if self.o == "^" or self.o == "v":
                self.turn_left()
            elif self.o == ">" or self.o == "<":
                self.turn_right()
        elif c == "+":
            if self.last is None or self.last == "right":
                self.turn_left()
                self.last = "left"
            elif self.last == "straight":
                self.turn_right()
                self.last = "right"
            else:
                self.last = "straight"

    def turn_left(self):
        ix = Map.orientations.index(self.o)
        ix = (ix + len(Map.orientations) - 1) % len(Map.orientations)
        self.o = Map.orientations[ix]

    def turn_right(self):
        ix = Map.orientations.index(self.o)
        ix = (ix + 1) % len(Map.orientations)
        self.o = Map.orientations[ix]


def move_while_no_collisions(map):
    while True:

        # Cart movement order is from top to bottom, left to right
        map.carts.sort(key=lambda c: c.location)

        for cart in map.carts:
            cart.move(map)

            collisions = get_collisions(map.carts)

            if len(collisions) != 0:
                return collisions


def move_while_more_than_one_remain(map):
    while len(map.carts) > 1:

        # Cart movement order is from top to bottom, left to right
        map.carts.sort(key=lambda c: c.location)

        # Move *all* carts, but when collided do not count in further collisions
        for cart in map.carts:
            cart.move(map)

            collisions = get_collisions(map.carts)
            for c in collisions:
                c.broken = True

        # Remove all broken carts from list so ordering stays correct
        map.carts = [c for c in map.carts if not c.broken]

    return map.carts[0]


def test():
    INPUT = ["/->-\         ",
             "|   |  /----\ ",
             "| /-+--+-\  | ",
             "| | |  | v  | ",
             "\-+-/  \-+--/ ",
             "  \------/    "]

    map = Map(INPUT)
    map.prepare()

    c = move_while_no_collisions(map)

    map.print()

    assert c[0].location.x == 7 and c[0].location.y == 3


def first():
    map = Map(get_input())
    map.prepare()

    c = move_while_no_collisions(map)

    return c[0].location


def second():
    # INPUT = ["/>-<\   ",
    #          "|   |   ",
    #          "| /<+-\ ",
    #          "| | | v ",
    #          "\>+</ | ",
    #          "  |   ^ ",
    #          "  \<->/ "]

    map = Map(get_input())
    map.prepare()

    cart = move_while_more_than_one_remain(map)

    return cart.location


if __name__ == "__main__":
    test()
    print("Collision at: {0}".format(first()))
    print("Last cart is at: {0}".format(second()))
