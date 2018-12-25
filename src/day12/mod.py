INPUT = ["##.#..########..##..#..##.....##..###.####.###.##.###...###.##..#.##...#.#.#...###..###.###.#.#",
         "####. => #",
         "##.#. => .",
         ".##.# => .",
         "..##. => .",
         "..... => .",
         ".#.#. => #",
         ".###. => .",
         ".#.## => .",
         "#.#.# => .",
         ".#... => #",
         "#..#. => #",
         "....# => .",
         "###.. => .",
         "##..# => #",
         "#..## => #",
         "..#.. => .",
         "##### => .",
         ".#### => #",
         "#.##. => #",
         "#.### => #",
         "...#. => .",
         "###.# => .",
         "#.#.. => #",
         "##... => #",
         "...## => #",
         ".#..# => .",
         "#.... => .",
         "#...# => .",
         ".##.. => #",
         "..### => .",
         "##.## => .",
         "..#.# => #"]


# INPUT = ["#..#.#..##......###...###",
#          "...## => #",
#          "..#.. => #",
#          ".#... => #",
#          ".#.#. => #",
#          ".#.## => #",
#          ".##.. => #",
#          ".#### => #",
#          "#.#.# => #",
#          "#.### => #",
#          "##.#. => #",
#          "##.## => #",
#          "###.. => #",
#          "###.# => #",
#          "####. => #"]


class Generation:
	def __init__(self, s):
		self.match = s[0:5]
		self.plant = s[9]

	def apply(self, next_state, current_state):
		# Assume next_state and current_state have enough leading and trailing empty pots to match at begin and end
		o = 0
		next_state = list(next_state)
		while o != -1:
			o = current_state.find(self.match, o)
			if o != -1:
				next_state[o + 2] = self.plant
				o += 1

		return "".join(next_state)


def assure_leading_and_trailing_pots(state, offset):
	"""
	Make sure there are enough empty pots at begin and end to match
	:param offset:  Index of pot #0
	"""

	ix = state.find("#")
	if ix != -1 and ix < 3:
		state = "." * (3 - ix) + state
		offset += (3 - ix)

	return state.rstrip(".") + "...", offset


def sum_plants(state, offset):
	r = 0

	ix = 0
	while ix != -1:
		ix = state.find("#", ix)
		if ix != -1:
			r += (ix - offset)
			ix += 1

	return r


def grow(state, generations, years):
	offset = 0
	for s in range(years):

		state, offset = assure_leading_and_trailing_pots(state, offset)

		next_state = "." * len(state)

		for g in generations:
			next_state = g.apply(next_state, state)

		state = next_state

	# print("{0:02d} ({2}):  {1}".format(s + 1, state, offset))

	return state, offset


def test():
	state = INPUT[0]
	generations = [Generation(s) for s in INPUT[1:]]

	state, offset = grow(state, generations, 20)

	print("({1}):  {0} {2}".format(state, offset, sum_plants(state, offset)))

	assert (sum_plants(state, offset) == 325)


def first():
	current_state = INPUT[0]
	generations = [Generation(s) for s in INPUT[1:]]

	current_state, offset = grow(current_state, generations, 20)

	print("({1}):  {0}".format(current_state, offset))

	return sum_plants(current_state, offset)


def second():
	current_state = INPUT[0]
	generations = [Generation(s) for s in INPUT[1:]]

	current_state, offset = grow(current_state, generations, 50000000000)

	print("({1}):  {0}".format(current_state, offset))

	return sum_plants(current_state, offset)


if __name__ == "__main__":
	# test()

	print("Sum of plants after 20 generations: {0}".format(first()))
	print("Sum of plants after 50 billion generations: {0}".format(second()))
