INPUT = ["Step V must be finished before step H can begin.",
         "Step U must be finished before step R can begin.",
         "Step E must be finished before step D can begin.",
         "Step B must be finished before step R can begin.",
         "Step W must be finished before step X can begin.",
         "Step A must be finished before step P can begin.",
         "Step T must be finished before step L can begin.",
         "Step F must be finished before step C can begin.",
         "Step P must be finished before step Y can begin.",
         "Step N must be finished before step G can begin.",
         "Step R must be finished before step S can begin.",
         "Step D must be finished before step C can begin.",
         "Step O must be finished before step K can begin.",
         "Step L must be finished before step J can begin.",
         "Step J must be finished before step H can begin.",
         "Step M must be finished before step I can begin.",
         "Step G must be finished before step K can begin.",
         "Step Z must be finished before step Q can begin.",
         "Step X must be finished before step Q can begin.",
         "Step H must be finished before step I can begin.",
         "Step K must be finished before step Y can begin.",
         "Step Q must be finished before step S can begin.",
         "Step I must be finished before step Y can begin.",
         "Step S must be finished before step Y can begin.",
         "Step C must be finished before step Y can begin.",
         "Step T must be finished before step S can begin.",
         "Step P must be finished before step S can begin.",
         "Step I must be finished before step S can begin.",
         "Step V must be finished before step O can begin.",
         "Step O must be finished before step Q can begin.",
         "Step T must be finished before step R can begin.",
         "Step E must be finished before step J can begin.",
         "Step F must be finished before step S can begin.",
         "Step O must be finished before step H can begin.",
         "Step Z must be finished before step S can begin.",
         "Step D must be finished before step Z can begin.",
         "Step F must be finished before step K can begin.",
         "Step W must be finished before step P can begin.",
         "Step G must be finished before step I can begin.",
         "Step B must be finished before step T can begin.",
         "Step G must be finished before step Y can begin.",
         "Step X must be finished before step S can begin.",
         "Step B must be finished before step K can begin.",
         "Step V must be finished before step A can begin.",
         "Step U must be finished before step N can begin.",
         "Step T must be finished before step P can begin.",
         "Step V must be finished before step D can begin.",
         "Step G must be finished before step X can begin.",
         "Step B must be finished before step D can begin.",
         "Step R must be finished before step J can begin.",
         "Step M must be finished before step Z can begin.",
         "Step U must be finished before step Z can begin.",
         "Step U must be finished before step G can begin.",
         "Step A must be finished before step C can begin.",
         "Step H must be finished before step Q can begin.",
         "Step X must be finished before step K can begin.",
         "Step B must be finished before step S can begin.",
         "Step Q must be finished before step C can begin.",
         "Step Q must be finished before step Y can begin.",
         "Step R must be finished before step I can begin.",
         "Step V must be finished before step Q can begin.",
         "Step A must be finished before step D can begin.",
         "Step D must be finished before step S can begin.",
         "Step K must be finished before step S can begin.",
         "Step G must be finished before step C can begin.",
         "Step D must be finished before step O can begin.",
         "Step R must be finished before step H can begin.",
         "Step K must be finished before step Q can begin.",
         "Step W must be finished before step R can begin.",
         "Step H must be finished before step Y can begin.",
         "Step P must be finished before step J can begin.",
         "Step N must be finished before step Z can begin.",
         "Step J must be finished before step K can begin.",
         "Step W must be finished before step M can begin.",
         "Step A must be finished before step Z can begin.",
         "Step V must be finished before step W can begin.",
         "Step J must be finished before step X can begin.",
         "Step U must be finished before step F can begin.",
         "Step P must be finished before step L can begin.",
         "Step W must be finished before step G can begin.",
         "Step T must be finished before step F can begin.",
         "Step R must be finished before step C can begin.",
         "Step R must be finished before step O can begin.",
         "Step Z must be finished before step C can begin.",
         "Step E must be finished before step S can begin.",
         "Step L must be finished before step I can begin.",
         "Step U must be finished before step O can begin.",
         "Step W must be finished before step K can begin.",
         "Step K must be finished before step I can begin.",
         "Step O must be finished before step M can begin.",
         "Step V must be finished before step M can begin.",
         "Step V must be finished before step Z can begin.",
         "Step A must be finished before step I can begin.",
         "Step F must be finished before step J can begin.",
         "Step F must be finished before step O can begin.",
         "Step M must be finished before step C can begin.",
         "Step Q must be finished before step I can begin.",
         "Step H must be finished before step S can begin.",
         "Step U must be finished before step A can begin.",
         "Step J must be finished before step S can begin.",
         "Step P must be finished before step Z can begin.", ]


# INPUT = [
#     "Step C must be finished before step A can begin.",
#     "Step C must be finished before step F can begin.",
#     "Step A must be finished before step B can begin.",
#     "Step A must be finished before step D can begin.",
#     "Step B must be finished before step E can begin.",
#     "Step D must be finished before step E can begin.",
#     "Step F must be finished before step E can begin.",
# ]


class NodeRule:

    def __init__(self, str):
        import re

        compiled = re.compile("""Step (\\w).*step (\\w) can begin.""")

        matches = compiled.match(str)
        self.node_id = matches.group(2)
        self.parent_id = matches.group(1)

    def __str__(self):
        return "{0} -> {1}".format(self.parent_id, self.node_id)


class Node:
    IDLE = 0
    ACTIVE = 1
    COMPLETE = 2

    def __init__(self, id):
        self.id = id
        self.parent_ids = set()
        self.parents = list()
        self.order = 0
        self.progress = 0
        self.state = Node.IDLE

    def is_done(self, timed=False):
        return (not timed and self.order != 0) or \
               (timed and self.progress >= self.processing_time())

    def parents_are_done(self, timed=False):
        r = True
        for parent in self.parents:
            r = r and parent.is_done(timed)
        return r

    def processing_time(self):
        return ord(self.id) - ord('A') + 1 + 60

    def __str__(self):
        return "{0} {1} [{2}] ".format(self.id, self.order, self.processing_time())


def build_node_list():
    """
    Build a list of nodes with parents for each node pointing at ehm, ...nodes
    :return: That list
    """
    node_rules = [NodeRule(line) for line in INPUT]

    # Build a dict of unique nodes with parent ids
    nodes = dict()
    for rule in node_rules:
        if rule.node_id not in nodes:
            nodes[rule.node_id] = Node(rule.node_id)
        if rule.parent_id not in nodes:
            nodes[rule.parent_id] = Node(rule.parent_id)

        node = nodes[rule.node_id]
        node.parent_ids.add(rule.parent_id)

    for node in nodes.values():
        node.parents = [nodes[parent_id] for parent_id in node.parent_ids]
        del node.parent_ids

    return [node for node in nodes.values()]


def first():
    nodes = build_node_list()
    nodes.sort(key=lambda n: n.id)

    order = 1
    complete = False
    while not complete:
        complete = True
        for node in nodes:
            if not node.is_done() and node.parents_are_done():
                complete = False
                node.order = order
                order += 1
                break  # Restart from the top

    nodes.sort(key=lambda n: n.order)

    return "".join([node.id for node in nodes])


def second():
    nodes = build_node_list()
    nodes.sort(key=lambda n: n.id)

    workers_available = 5

    order = 1
    elapsed = 0  # Total elapsed time

    # Repeat as long as there are unfinished nodes
    while any(node.state != Node.COMPLETE for node in nodes):

        # If any nodes are startable and workers are available then start them
        for node in nodes:
            if node.state == Node.IDLE:
                if node.parents_are_done(timed=True):
                    if workers_available > 0:
                        workers_available -= 1
                        node.state = Node.ACTIVE

        # For ACTIVE nodes keep progress and finish them if completed
        for node in nodes:
            if node.state == Node.ACTIVE:
                node.progress += 1

                if node.is_done(timed=True):
                    node.state = Node.COMPLETE
                    node.order = order
                    order += 1
                    workers_available += 1

        elapsed += 1

    nodes.sort(key=lambda n: n.order)

    return "".join((node.id for node in nodes)), elapsed


if __name__ == "__main__":
    print("Correct order : {0}".format(first()))
    print("Correct order : {0} completed in {1}[s]".format(*second()))
