import re

pattern = re.compile(r"(\w)=(\d*),.*(\w)=(\d*)\.\.(\d*)")


class Region:
    def __init__(self, line, fill):
        matches = pattern.match(line)

        if line.startswith('x'):
            self.x = range(int(matches.group(2)), int(matches.group(2)) + 1)
            self.y = range(int(matches.group(4)), int(matches.group(5)) + 1)
        elif line.startswith('y'):
            self.y = range(int(matches.group(2)), int(matches.group(2)) + 1)
            self.x = range(int(matches.group(4)), int(matches.group(5)) + 1)

        self.fill = fill

    def x_min(self):
        return self.x[0]

    def x_max(self):
        return self.x[-1]

    def y_min(self):
        return self.y[0]

    def y_max(self):
        return self.y[-1]

    @staticmethod
    def clay(line):
        return Region(line, "#")

    @staticmethod
    def well(line):
        return Region(line, "+")

    @staticmethod
    def is_clay(fill):
        return fill == '#'

    @staticmethod
    def is_water(fill):
        return fill == '~'

    @staticmethod
    def was_water(fill):
        return fill == '|'

    @staticmethod
    def is_well(fill):
        return fill == '+'


class Map:
    def __init__(self, top_left, bottom_right):
        self.top_Left = top_left
        self.bottom_right = bottom_right
        self.map = [['.'] * (1 + bottom_right[0] - top_left[0]) for _ in range(1 + bottom_right[1] - top_left[1])]

    def __getitem__(self, location):
        return self.map[location[1] - self.top_Left[1]][location[0] - self.top_Left[0]]

    def __setitem__(self, location, value):
        self.map[location[1] - self.top_Left[1]][location[0] - self.top_Left[0]] = value

    def __str__(self):
        return "\n".join("".join(line) for line in self.map)

    def apply_region(self, region):
        for y in region.y:
            for x in region.x:
                self[(x, y)] = region.fill

    def water(self):
        # Iterate from last but one @bottom to top
        for y in range(self.bottom_right[1] - 1, self.top_Left[1] - 1, -1):

            # Iterate from leftmost column to rightmost column
            for x in range(self.top_Left[0], self.bottom_right[0] + 1):

                current = self[(x, y)]
                left = self[(x - 1, y)]
                right = self[(x + 1, y)]
                below = self[(x, y + 1)]

                if Region.is_water(current):
                    pass
                elif Region.is_clay(current):
                    pass


def get_input():
    with open("input.txt", "r") as f:
        return f.readlines()


def regions_add_well(regions):
    regions.append(Region.well("x=500,y=0..0"))


def regions_find_extends(regions):
    top_left = (min([r.x_min() for r in regions]), min([r.y_min() for r in regions]))
    bottom_right = (max([r.x_max() for r in regions]), max([r.y_max() for r in regions]))

    return top_left, bottom_right


def create_map(inp):
    regions = [Region.clay(line) for line in inp]
    regions_add_well(regions)

    top_left, bottom_right = regions_find_extends(regions)

    map = Map(top_left, bottom_right)
    for region in regions:
        map.apply_region(region)

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

    map[map.top_Left] = "!"
    map[map.bottom_right] = "@"
    print(map)


def first():
    map = create_map(get_input())
    print(map)


def second():
    pass


if __name__ == "__main__":
    test()
    print("Number of tiles the water can reach: {0}".format(first()))
    print("Some other graph questions answer: {0}".format(second()))
