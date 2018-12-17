def get_input():
    with open("input.txt", "r") as f:
        return f.read().split()


class Node:
    def __init__(self, lvl, cc, mc):
        self.nr = lvl
        self.cc = cc
        self.mc = mc
        self.meta = list()

    def __str__(self):
        return "{3:03d}: {0:03d} {1:03d}->{2}".format(self.cc, self.mc, self.meta, self.nr)


def parse_nodes(dst, lvl, inp):
    """
    Recursively traverse the inp parsing nodes and putting them in dst
    :return: dst with added nodes and unparsed input
    """
    if len(inp) == 0:
        return dst, inp

    # Fixed piece
    cc = int(inp[0])
    mc = int(inp[1])

    node = Node(lvl, cc, mc)
    dst.append(node)

    # Remove fixed piece and parse children if any
    inp = inp[2:]
    for c in range(0, cc):
        dst, inp = parse_nodes(dst, lvl + 1, inp)

    # inp is unparsed input, so this contains the meta part we aer still missing
    node.meta = [int(c) for c in inp[:mc]]

    # .. and remove the meta part
    inp = inp[mc:]

    return dst, inp


def first():
    nodes, _ = parse_nodes(list(), 0, get_input())

    return sum(sum(node.meta) for node in nodes)


def second():
    return 0


if __name__ == "__main__":
    print("Meta sum : {0}".format(first()))
    print("Correct order : {0}".format(second()))
