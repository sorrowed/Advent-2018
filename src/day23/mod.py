import re
import heapq

parse_nanobot = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "({0},{1},{2})".format(self.x, self.y, self.z)

    @staticmethod
    def manhattan_distance_to_point(a, b):
        return abs(b.x - a.x) + abs(b.y - a.y) + abs(b.z - a.z)

    @staticmethod
    def manhattan_distance_to_region(point, origin, width, height, depth):
        def distance_to_segment(mn, mx, p):
            return mn - p if mn > p else p - mx if p > mx else 0

        return distance_to_segment(origin.x, origin.x + width - 1, point.x) + \
               distance_to_segment(origin.y, origin.y + height - 1, point.y) + \
               distance_to_segment(origin.z, origin.z + depth - 1, point.z)


class Nanobot:
    def __init__(self, x, y, z, r):
        self.origin = Point(x, y, z)
        self.r = r

    def in_range(self, other):
        return Point.manhattan_distance_to_point(self.origin,
                                                 other.origin) <= self.r  # and other.distance(self) <= other.r

    def __str__(self):
        return "{}->{}".format(self.origin, self.r)


class Region:
    def __init__(self, x, y, z, width, height, depth, bots):
        self.origin = Point(x, y, z)
        self.width = width
        self.height = height
        self.depth = depth
        self.bots = bots
        self.key = (-len(self.bots), Point.manhattan_distance_to_point(self.origin, Point(0, 0, 0)))

    def split(self):
        width = int(self.width / 2) if self.width > 1 else 1
        height = int(self.height / 2) if self.height > 1 else 1
        depth = int(self.depth / 2) if self.depth > 1 else 1

        sub_regions = list()
        for z in (self.origin.z, self.origin.z + depth):
            for y in (self.origin.y, self.origin.y + height):
                for x in (self.origin.x, self.origin.x + width):
                    bots = [bot for bot in self.bots if
                            Point.manhattan_distance_to_region(bot.origin, Point(x, y, z), width, height,
                                                               depth) <= bot.r]

                    region = Region(x, y, z, width, height, depth, bots)

                    sub_regions.append(region)

        return sub_regions

    def __lt__(self, other):
        return self.key < other.key

    def __str__(self):
        return "Region: {},({},{},{} : {} bots)".format(self.origin, self.width, self.height, self.depth,
                                                        len(self.bots))


def get_input():
    with open("input.txt", "r") as f:
        return f.readlines()


def parse_nanobot_data(s):
    matches = parse_nanobot.match(s)
    return Nanobot(*map(int, matches.groups()))


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

    origins = [nb.origin for nb in nanobots]

    x_min, x_max = min(origins, key=lambda o: o.x).x, max(origins, key=lambda o: o.x).x
    y_min, y_max = min(origins, key=lambda o: o.y).y, max(origins, key=lambda o: o.y).y
    z_min, z_max = min(origins, key=lambda o: o.z).z, max(origins, key=lambda o: o.z).z

    r = None
    queue = []
    heapq.heappush(queue,
                   Region(x_min, y_min, z_min, x_max - x_min + 1, y_max - y_min + 1, z_max - z_min + 1, nanobots))
    while r is None:
        region = heapq.heappop(queue)
        if region.width == 1:  # Assume cube here. Whatever ....
            r = region
        else:
            regions = region.split()
            [heapq.heappush(queue, region) for region in regions]

    # Should return distance: 98565591, bots in range: 975, pos: (17304966, 29121001, 52139624)
    return Point.manhattan_distance_to_point(Point(0, 0, 0), r.origin)


if __name__ == "__main__":
    test()
    print("Nanobots in range of strongest: {0}".format(first()))
    print("Distance to origin of point with largest number of nanobots in range: {0}".format(second()))
