import sys

INPUT = """473 players; last marble is worth 70904 points"""

PLAYER_COUNT = 473
LAST_MARBLE_VALUE = 70904


# PLAYER_COUNT = 9
# LAST_MARBLE_VALUE = 26

class Marble:
    def __init__(self, id):
        self.id = id
        self.next = self
        self.prev = self

    def __str__(self):
        return "{0}-->".format(self.id) if self.next.id != self.id else "{0}".format(self.id)


def insert_marble(after, m):
    m.next = after.next
    after.next = m
    m.prev = after
    m.next.prev = m

    return m


def remove_marble(m):
    prev = m.prev
    nxt = m.next

    nxt.prev = prev
    prev.next = nxt

    return nxt


def print_marbles(marble):
    begin = marble
    while True:

        sys.stdout.write(str(marble))
        marble = marble.next
        if marble == begin:
            break
    print("")


def play(players, last_marble):
    scores = dict((player_id, 0) for player_id in range(1, players + 1))

    current_marble = Marble(0)
    for id in range(1, last_marble):
        marble = Marble(id)

        if (id % 23) != 0:
            current_marble = current_marble.next
            current_marble = insert_marble(current_marble, marble)
        else:

            scores[1 + (id % players)] += marble.id

            for _ in range(0, 7):
                current_marble = current_marble.prev

            scores[1 + (id % players)] += current_marble.id

            current_marble = remove_marble(current_marble)

    return scores


def first():
    return max(play(PLAYER_COUNT, LAST_MARBLE_VALUE).values())


def second():
    return max(play(PLAYER_COUNT, LAST_MARBLE_VALUE * 100).values())


if __name__ == "__main__":
    print("Winning score : {0}".format(first()))
    print("Winning score : {0}".format(second()))
