def get_input():
    with open("input.txt", "r") as f:
        return f.readlines()


class Location:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Map:
    def __init__(self, lines):
        self.lines = lines
        self.carts = list()

    def prepare(self):
        pass

    def __getitem__(self, location):
        pass


class Cart:
    orientations = ["^", ">", "v", "<"]

    def __init__(self, location, o, limits):
        self.location = location
        self.o = o
        self.limits = limits
        self.last = None

    def move(self, c):
        if c == "+":
            if self.last is None or self.last == "right":
                self.o = self.turn_left(self.o)
                self.last = "left"
            elif self.last == "straight":
                self.o = self.turn_right(self.o)
                self.last = "right"
            else:
                self.last = "straight"

        if self.o == "^":
            self.location.y -= 1
        elif self.o == ">":
            self.location.x += 1
        elif self.o == "v":
            self.location.y += 1
        elif self.o == "<":
            self.location.x -= 1

        self.limits()

        self.o = self.orientation(c)

    def orientation(self, c):
        if c == "/":
            if self.o == "^":
                c = ">"
            elif c == "v":
                c = "<"
            elif c == ">":
                c = "^"
            elif c == "<":
                c = "v"
        elif self.o == "\\":
            if c == "^":
                c = "<"
            elif c == ">":
                c = "<"
            elif c == ">":
                c = "v"
            elif c == "<":
                c = "^"
        return c

    def turn_left(self):
        ix = Cart.orientations.index(self.o)
        ix -= 1
        if ix < 0:
            ix = len(Cart.orientations) - 1
        return Cart.orientations[ix]

    def turn_right(self):
        ix = Cart.orientations.index(self.o)
        ix = (ix + 1) % len(Cart.orientations)
        return Cart.orientations[ix]

    def limits(self):
        if self.location.x <= 0:
            self.location.x = 0
        if self.location.x >= self.limits.x:
            self.location.x = self.limits.x
        if self.location.y <= 0:
            self.location.y = 0
        if self.location.y >= self.limits.y:
            self.location.y = self.limits.y


def first():
    map = Map(get_input())
    map.prepare()


def second():
    pass


if __name__ == "__main__":
    print("")
    print("")
