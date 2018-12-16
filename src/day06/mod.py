from collections import namedtuple

INPUT = [(264, 340, 'A'), (308, 156, 'B'), (252, 127, 'C'), (65, 75, 'D'), (102, 291, 'E'), (47, 67, 'F'),
         (83, 44, 'G'), (313, 307, 'H'), (159, 48, 'I'), (84, 59, 'J'), (263, 248, 'K'), (188, 258, 'L'),
         (312, 240, 'M'), (59, 173, 'N'), (191, 130, 'O'), (155, 266, 'P'), (252, 119, 'Q'), (108, 299, 'R'),
         (50, 84, 'S'), (172, 227, 'T'), (226, 159, 'U'), (262, 177, 'V'), (233, 137, 'W'), (140, 211, 'X'),
         (108, 175, 'Y'), (278, 255, 'Z'), (259, 209, '['), (233, 62, '*'), (44, 341, ']'), (58, 175, '^'),
         (252, 74, '_'), (232, 63, '`'), (176, 119, 'a'), (209, 334, 'b'), (103, 112, 'c'), (155, 94, 'd'),
         (253, 255, 'e'), (169, 87, 'f'), (135, 342, 'g'), (55, 187, 'h'), (313, 338, 'i'), (210, 63, 'j'),
         (237, 321, 'k'), (171, 143, 'l'), (63, 238, 'm'), (79, 132, 'n'), (135, 113, 'o'), (310, 294, 'p'),
         (289, 184, 'q'), (56, 259, 'r')]

Coordinate = namedtuple('Coordinate', ["x", "y", "id"])
Location = namedtuple('Location', ["coordinate", "distance"])


def distance(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def make_key(x, y):
    return y << 16 | x


def make_limits():
    return min(INPUT, key=lambda c: c[0])[0], max(INPUT, key=lambda c: c[0])[0], min(INPUT, key=lambda c: c[1])[1], \
           max(INPUT, key=lambda c: c[1])[1]


def print_field(fld, x_min, x_max, y_min, y_max):
    import sys
    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            sys.stdout.write("{0}".format(fld[make_key(x, y)].id))
        sys.stdout.write("\n")


def first():
    x_min, x_max, y_min, y_max = make_limits()

    # So i can print something on a location that is not owned by anyone
    no_coordinate = Coordinate(x=-1, y=-1, id='.')

    # Register all unique owners
    owner_ids = set((inp[2] for inp in INPUT))
    edge_ids = set()
    field = dict()
    for x in range(x_min, x_max):
        for y in range(y_min, y_max):

            # Calculate distance between (x,y) and all input locations
            # Element[0] is the location, element[1] the distance FIXME: namedtuple
            distances = [Location(coordinate=Coordinate(x=inp[0], y=inp[1], id=inp[2]), distance=distance([x, y], inp))
                         for inp in INPUT]

            # Sort ascending
            distances.sort(key=lambda l: l.distance)

            # Input location with smallest distance (if there is only one) is the owner
            if len(distances) == 1 or distances[0].distance != distances[1].distance:
                field[make_key(x, y)] = distances[0].coordinate

                # Keep track of owners that are on edges as they're infinitely large
                is_edge = lambda x, y: x <= x_min or x >= x_max or y <= y_min or y >= y_max

                if is_edge(x, y):
                    edge_ids.add(distances[0].coordinate.id)

            else:
                field[make_key(x, y)] = no_coordinate

    # Prints the map
    print_field(field, x_min, x_max, y_min, y_max)

    # For each owner id which is not an edge id, count the number of occurrences in field.values
    counts = [(id, len([x for x in field.values() if x.id == id])) for id in owner_ids if id not in edge_ids]

    # Return the count of the owner id that is most prominent in the map
    return max(counts, key=lambda c: c[1])[1]


def second():
    x_min, x_max, y_min, y_max = make_limits()

    # Make sum of distance to input for each location
    field = dict()
    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            field[make_key(x, y)] = sum([distance([x, y], inp) for inp in INPUT])

    # Select the ones that are closer than 10000
    selection = {(k, v) for (k, v) in field.items() if v < 10000}

    return len(selection)


if __name__ == "__main__":
    print("Size of largest none-edge region : {0}".format(first()))
    print("Size of region with distance < 10000: {0}".format(second()))
