def get_input():
    # return [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]

    with open("input.txt", "r") as f:
        return f.read().split()


class Node:
    def __init__(self, lvl, cc, mc):
        self.nr = lvl
        self.cc = cc
        self.mc = mc
        self.meta = list()
        self.children = list()

    def get_value_pt1(self):
        return sum(self.meta)

    def get_value_pt2(self):
        """
        Return part 1 value if no children, else use meta content as child indices ( filter values to range
        [1..len(self.children)] ) and sum their pt2 values. Return that
        :return: Yes, when done.
        """
        return self.get_value_pt1() if len(self.children) == 0 else \
            sum(child.get_value_pt2() for child in
                [self.children[m - 1] for m in self.meta if 0 < m <= len(self.children)])

    def __str__(self):
        return "{3:03d}: {0:03d} {1:03d}->{2}".format(self.cc, self.mc, self.meta, self.nr)


def parse_nodes(parent, dst, lvl, inp):
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
    if parent is not None:
        parent.children.append(node)

    dst.append(node)

    # Remove fixed piece and parse children if any
    inp = inp[2:]
    for c in range(0, cc):
        dst, inp = parse_nodes(node, dst, lvl + 1, inp)

    # inp is unparsed input, so this starts with the meta part we are still missing
    node.meta = [int(c) for c in inp[:mc]]

    # .. and remove the meta part
    inp = inp[mc:]

    return dst, inp


def first():
    nodes, _ = parse_nodes(None, list(), 0, get_input())

    return sum(node.get_value_pt1() for node in nodes)


def second():
    nodes, _ = parse_nodes(None, list(), 0, get_input())

    return nodes[0].get_value_pt2()


if __name__ == "__main__":
    print("Meta sum : {0}".format(first()))
    print("Meta sum : {0}".format(second()))
