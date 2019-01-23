INPUT = [".|....|.|.#|.#..|.#..||#..|.||#|#|||.....#......#.",
         ".....||..||.|#.......#.|.....|....#..|..|.|.#..|.#",
         ".#.#......|#.#..|......|.......|.|.|..#.#......#|.",
         ".#.....#..|..#..|#..|#|......#...#||.|...##...#..|",
         "|......|..#.#.#....|..#..#..#|##....#.....|.|#..#.",
         ".....|..#....#..|.#.....|..#...|###.|||###...#.||.",
         "|...##.#..|...||.....#.|.#|#|........#.|#|..|..#.|",
         ".....|......|........#...#..|||||#|#||.|...|...#..",
         ".....||..#.||.......|..|.|##..##|#..|.#..|#.##.#..",
         ".|#.#|..||.|.|.|..|.|...|#.|.|..##.|#.#..|...|#||.",
         ".|||....#||##..#.....|#...#....|.#|..#|.|...|###.#",
         "#...|....|......#..#.#......||.||....#|##....#|#|#",
         "|.|....#.#|#..|....|.#...|.|||.|.|#|....#..|......",
         "#...|.....#...#|................|..#||#|....#.....",
         "..||....#..|.....|||..#|...|#|.#.|..#|..|.|#|....#",
         "....##|##|.|#.#.|||#.#..|...#|.|.###.#.|......|||#",
         ".....##|.|.#...#..#.........|..|...#.|...#...|....",
         "##.#.#...#.|..|||#...||..#|#.#||#|#|..#.##....|...",
         "#.|..#||.|#|....#...##.....|.#..#....|...|#.|#....",
         "||.##...|...|..|...#......|.##.#.#|..#.#.|.......#",
         "#....#|..#.......|||......|..#........|..|..#..|..",
         ".|.........####..|.|....#....##.|....|...#|.|.||..",
         "......##|#.#...#...|||......|.#.|||...||........|.",
         "#.|..|...#.#....#|......||......|.....#...#....#..",
         "...|.|#|#.............#.||.|..|####..|..#.##|.||#.",
         "..#..|...||#....#.#..#.|..|#|.||.#...|||#..#|..#..",
         "#|#|..||#|.|..|...|.....#..#..#..|#.|#....|.||||..",
         "....##||...|#|..#.|#....|...|.#.|...#...|#.##.#.#.",
         "...|||||.#...###.|#.|.|......#...|...|...##.#.#|.|",
         "|.|..##...|...|.......||..|..#.#|..|.|#|||....||..",
         "..|.#|.#.|.|..|.#.|.##..|..|.#|.......#.....#.#.|.",
         "...#...|..#.........#..##...........#....|..#.....",
         ".#...|....|#|#.##.......#......|#..|.|...........#",
         "|......#.#||.#.||..|......|....#..#|...##...|#...|",
         "|.#..##||.........|||.#.#.##|#||##......|||.#..##|",
         "|...|.|#|...#.##|..#..#||||||.||#|.#...#|....#|.||",
         "||#..|.#.......||.|....#..|..|#.......#||.|##|....",
         "|.|..#.||##...##.....#............||.|#|.....##...",
         "#.#..|..||.|.|#.......#|..#..|.#|........#.##.####",
         "...#.|.|.#|...#.#..|.....|.#.#.|......#|.||.|.....",
         ".|.##...#.#||.##.#.||...#...|||...|.##..##..|##...",
         "..##.|...#....|.#..||....|..##..#|.||...#..#......",
         "...##.#.|||......|..|#.|..#.|#.....|#|....#..#|.#|",
         ".#.||.|#.##..||.#.||||#..##.##..#.....#.##.#.#.#.|",
         ".#|#|.....#..#..##.......|.|#|....#.........#|....",
         "#....|.#..|.#|##.##...|...|..#.|....#.#.||.#.#....",
         ".####|.....|.|..#...|.#|#...#...||.#|.|.|..|#.....",
         "##|#.#.........|.......#...#....||#|..|##...#.#|.#",
         "###||#.#|....#.......|...#.#.#....|#|#|#..|..|#|#.",
         ".|...#..#..|.....##|#....|||#..#...|..#.|...|##|.."]


class Map:
    def __init__(self, src):
        self.height = len(src)
        self.width = len(src[0])

        self.map = [['.'] * self.width for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                self[x, y] = src[y][x]

    def __getitem__(self, loc):
        return self.map[loc[1]][loc[0]]

    def __setitem__(self, loc, v):
        self.map[loc[1]][loc[0]] = v

    def __str__(self):
        s = str()
        for row in self.map:
            s += "".join([s for s in row]) + "\n"

        return s

    @staticmethod
    def is_open(c):
        return c == "."

    @staticmethod
    def is_tree(c):
        return c == "|"

    @staticmethod
    def is_lumberyard(c):
        return c == "#"

    def adjacent(self, loc):
        r = list()
        for y in [loc[1] - 1, loc[1], loc[1] + 1]:
            for x in [loc[0] - 1, loc[0], loc[0] + 1]:
                if x == loc[0] and y == loc[1]:
                    continue

                if 0 <= x < self.width and 0 <= y < self.height:
                    r.append(self[(x, y)])
        return r

    @staticmethod
    def open(adjacent):
        return "|" if sum(1 for c in adjacent if c == "|") >= 3 else "."

    @staticmethod
    def trees(adjacent):
        return "#" if sum(1 for c in adjacent if c == "#") >= 3 else "|"

    @staticmethod
    def lumberyard(adjacent):
        return "#" if (sum(1 for c in adjacent if c == "#") >= 1 and sum(1 for c in adjacent if c == "|") >= 1) else "."

    def minute(self):
        n = Map(self.map)

        for y in range(self.height):
            for x in range(self.width):

                adjacent = self.adjacent((x, y))

                if Map.is_tree(self[(x, y)]):
                    n[(x, y)] = Map.trees(adjacent)
                if Map.is_open(self[(x, y)]):
                    n[(x, y)] = Map.open(adjacent)
                if Map.is_lumberyard(self[(x, y)]):
                    n[(x, y)] = Map.lumberyard(adjacent)

        return n

    def wooded(self):
        return sum(len([c for c in r if Map.is_tree(c)]) for r in self.map)

    def lumberyards(self):
        return sum(len([c for c in r if Map.is_lumberyard(c)]) for r in self.map)

    def value(self):
        return self.wooded() * self.lumberyards()


def test():
    inp = [".#.#...|#.",
           ".....#|##|",
           ".|..|...#.",
           "..|#.....#",
           "#.#|||#|#|",
           "...#.||...",
           ".|....|...",
           "||...#|.#|",
           "|.||||..|.",
           "...#.|..|."]
    map = Map(inp)
    print(map)

    for _ in range(10):
        map = map.minute()
        print(map)

    return map.value()


def first():
    map = Map(INPUT)
    for _ in range(10):
        map = map.minute()

    print(map)
    return map.value()


def minutes_forward_fast(tries, previous, current):
    """
    Forwards the minutes counter given that current minute and previous minute is a (stable!) repetition interval
    """
    return tries - (tries - current) % (current - previous)


def second():
    map = Map(INPUT)

    scores = dict()
    x = 0
    while x < 1000000000:
        map = map.minute()
        x += 1

        # After this many minutes a (stable!) map.value() interval (every 28 minutes) is established/observed.
        # Forward the minutes as close to the requested 1000000000 minutes deadline as possible
        if x >= 517 and scores is not None:
            v = map.value()
            if v in scores.keys():
                x = minutes_forward_fast(1000000000, scores[v], x)
                scores = None
            else:
                scores[v] = x

    print(map)
    return map.value()


if __name__ == "__main__":
    print("Resource value after 10 minutes in test input: {0}".format(test()))
    print("Resource value after 10 minutes in input: {0}".format(first()))
    print("Resource value after 1000000000 minutes in input: {0}".format(second()))
