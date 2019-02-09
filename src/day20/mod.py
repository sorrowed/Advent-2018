def get_input():
    with open("input.txt", "r") as f:
        return f.read()


class Location():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Location(self.x, self.y)

    def __str__(self):
        return "({0},{1})".format(self.x, self.y)


class Map:
    def __init__(self):
        self.map = dict()
        self.map[(0, 0)] = 'X'

    def __getitem__(self, c):
        return self.map[(c[0], c[1])]

    def __setitem__(self, c, v):
        self.map[(c[0], c[1])] = v

    def __str__(self):
        x_min = min(self.map.keys(), key=lambda k: k[0])[0]
        x_max = max(self.map.keys(), key=lambda k: k[0])[0]
        y_min = min(self.map.keys(), key=lambda k: k[1])[1]
        y_max = max(self.map.keys(), key=lambda k: k[1])[1]

        s = str()
        for y in range(y_min - 1, y_max + 2):  # Add border
            line = ""
            for x in range(x_min - 1, x_max + 2):
                if (x, y) in self.map:
                    line += self.map[(x, y)]
                else:
                    line += "#"

            s += line + "\n"

        return s


class Path:
    def __init__(self, x, y):
        self.current = Location(x, y)

    def step(self, c, m):

        current = self.current

        if c == "E":
            current.x += 1
            m[(current.x, current.y)] = "|"
            current.x += 1
        elif c == "N":
            current.y -= 1
            m[(current.x, current.y)] = "-"
            current.y -= 1
        elif c == "W":
            current.x -= 1
            m[(current.x, current.y)] = "|"
            current.x -= 1
        elif c == "S":
            current.y += 1
            m[(current.x, current.y)] = "-"
            current.y += 1

        m[(current.x, current.y)] = "."


def traverse(inp, m):
    stack = list()  # Path stack

    parent = Path(0, 0)

    for c in inp:
        if c == "^":
            pass
        elif c == "(":  # Start of path group, push parent on stack
            child = Path(parent.current.x, parent.current.y)
            stack.append(parent)
            parent = child
        elif c == "|":  # End of child path. Continue with another child path in group, use same parent
            parent = stack.pop()
            child = Path(parent.current.x, parent.current.y)
            stack.append(parent)
            parent = child
        elif c == ")" or c == "$":  # End of path group.
            if len(stack) > 0:
                parent = stack.pop()
        else:
            parent.step(c, m)  # Add step to current path


def test():
    inp = r"^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"

    m = Map()
    traverse(iter(inp), m)
    print(m)


def first():
    m = Map()

    traverse(get_input(), m)
    print(m)
    return 0


def second():
    pass


if __name__ == "__main__":
    test()
    print("Number of doors to furthest room: {0}".format(first()))

    # print("Dunno: {0}".format(second()))
