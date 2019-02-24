import re

parse_coordinate = re.compile(r"(-?\d+),(-?\d+),(-?\d+),(-?\d+)")


class Coordinate:
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def distance(self, c):
        return abs(self.a - c.a) + abs(self.b - c.b) + \
               abs(self.c - c.c) + abs(self.d - c.d)

    def __str__(self):
        return "({},{},{},{})".format(self.a, self.b, self.c, self.d)


class Constellation:
    def __init__(self, initial_coordinate):
        self.coordinates = [initial_coordinate]

    def merge(self, constellation):
        self.coordinates.extend(constellation.coordinates)
        constellation.clear()

    def clear(self):
        self.coordinates.clear()

    def in_range(self, coordinate):
        for c in self.coordinates:
            if c.distance(coordinate) <= 3:
                return True
        return False

    def __str__(self):
        return "Constellation with {} coordinates".format(len(self.coordinates))


def get_input():
    with open("input.txt", "r") as f:
        return f.readlines()


def parse_coordinates(inp):
    return [Coordinate(*map(int, parse_coordinate.match(s).groups())) for s in inp]


def assemble_constellations(coordinates):
    constellations = list()

    for coordinate in coordinates:
        matched = set()

        # Check which constellations are in range of coordinate
        for c in constellations:
            if c.in_range(coordinate):
                matched.add(c)

        # Create a new constellation with coordinate in it and merge all constellations in matched
        constellation = Constellation(coordinate)
        for c in matched:
            constellation.merge(c)
            constellations.remove(c)
        constellations.append(constellation)

    return constellations


def test():
    constellations = assemble_constellations(
        parse_coordinates(["0,0,0,0", "3,0,0,0", "0,3,0,0", "0,0,3,0", "0,0,0,3", "0,0,0,6", "9,0,0,0", "12,0,0,0"]))
    print(len(constellations))

    constellations = assemble_constellations(
        parse_coordinates(
            ["-1,2,2,0", "0,0,2,-2", "0,0,0,-2", "-1,2,0,0", "-2,-2,-2,2", "3,0,2,-1", "-1,3,2,2", "-1,0,-1,0",
             "0,2,1,-2", "3,0,0,0"]))
    print(len(constellations))

    constellations = assemble_constellations(
        parse_coordinates(
            ["1,-1,0,1", "2,0,-1,0", "3,2,-1,0", "0,0,3,1", "0,0,-1,-1", "2,3,-2,0", "-2,2,0,0", "2,-2,0,-1",
             "1,-1,0,-1", "3,2,0,2"]))
    print(len(constellations))

    constellations = assemble_constellations(
        parse_coordinates(
            ["1,-1,-1,-2", "-2,-2,0,1", "0,2,1,3", "-2,3,-2,1", "0,2,3,-2", "-1,-1,1,-2", "0,-2,-1,0", "-2,2,3,-1",
             "1,2,2,0", "-1,-2,0,-2"]))
    print(len(constellations))


def first():
    constellations = assemble_constellations(parse_coordinates(get_input()))
    return len(constellations)


def second():
    pass


if __name__ == "__main__":
    test()
    print("Number of constellations: {0}".format(first()))
    print("blerp: {0}".format(second()))
