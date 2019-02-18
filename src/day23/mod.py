import re

parse_nanobot = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")


class Nanobot:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = r

    def in_range(self, other):
        return self.distance(other) <= self.r  # and other.distance(self) <= other.r

    def distance(self, other):
        return abs(other.x - self.x) + abs(other.y - self.y) + abs(other.z - self.z)

    def __str__(self):
        return "({0},{1},{2})->{3}".format(self.x, self.y, self.z, self.r)


def get_input():
    with open("input.txt", "r") as f:
        return f.readlines()


def parse_nanobot_data(s):
    matches = parse_nanobot.match(s)
    return Nanobot(int(matches.group(1)), int(matches.group(2)), int(matches.group(3)), int(matches.group(4)))


def test():
    inp = ["pos=<0,0,0>, r=4", "pos=<1,0,0>, r=1", "pos=<4,0,0>, r=3",
           "pos=<0,2,0>, r=1", "pos=<0,5,0>, r=3", "pos=<0,0,3>, r=1",
           "pos=<1,1,1>, r=1", "pos=<1,1,2>, r=1", "pos=<1,3,1>, r=1"]

    nanobots = [parse_nanobot_data(s) for s in inp]

    strongest = max(nanobots, key=lambda nb: nb.r)

    in_range = [nb for nb in nanobots if strongest.in_range(nb)]

    print("Strongest nanobot:", strongest, "and", len(in_range), "in range")


def first():
    inp = get_input()
    nanobots = [parse_nanobot_data(s) for s in inp]

    strongest = max(nanobots, key=lambda nb: nb.r)

    print("Strongest nanobot: ", strongest)

    in_range = [nb for nb in nanobots if strongest.in_range(nb)]

    return len(in_range)


def second():
    """
    - Iterate all nanobots and construct a set with coordinates+counts that are in range
    - Keep the one closest to (0,0,0)
    """
    inp = get_input()
    nanobots = [parse_nanobot_data(s) for s in inp]

    x_min, x_max = min(nanobots, key=lambda nb: nb.x).x, max(nanobots, key=lambda nb: nb.x).x
    y_min, y_max = min(nanobots, key=lambda nb: nb.y).y, max(nanobots, key=lambda nb: nb.y).y
    z_min, z_max = min(nanobots, key=lambda nb: nb.z).z, max(nanobots, key=lambda nb: nb.z).z

    print(x_min, x_max, y_min, y_max, z_min, z_max)


if __name__ == "__main__":
    test()
    print("Nanobots in range of strongest: {0}".format(first()))
    print("Bieb".format(second()))
