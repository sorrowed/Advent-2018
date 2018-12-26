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
         "..#.# => #", ]


class Generation:
	def __init__(self, s):
		self.match = s[0:5]
		self.plant = s[9]

	def apply(self, next_state, current_state):
		# Assume next_state and current_state have enough leading and trailing empty pots to match at begin and end
		next_state = list(next_state)
		o = 0
		while True:
			o = current_state.find(self.match, o)
			if o != -1:
				next_state[o + 2] = self.plant
				o += 1
			else:
				break

		return "".join(next_state)


def assure_leading_and_trailing_pots(state, offset):
	"""
	Make sure there are enough empty pots at begin and end to match
	:param offset:  Index of pot #0
	"""

	ix = state.find("#")
	if ix != -1:
		state = "..." + state.lstrip(".")
		offset += (3 - ix)

	return state.rstrip(".") + "...", offset


def sum_plants(state, offset):
	r = 0

	ix = 0
	while True:
		ix = state.find("#", ix)
		if ix != -1:
			r += (ix - offset)
			ix += 1
		else:
			break

	return r


def grow(state, generations, years):
	offset = 0
	for s in range(years):

		state, offset = assure_leading_and_trailing_pots(state, offset)

		next_state = "." * len(state)

		for g in generations:
			next_state = g.apply(next_state, state)

		state = next_state

		print("{0:02d} ({2:+03d}) sum({3}):  {1}".format(s + 1, state, offset, sum_plants(state, offset)))

	return state, offset


def test():
	TEST_INPUT = ["#..#.#..##......###...###",
	              "...## => #",
	              "..#.. => #",
	              ".#... => #",
	              ".#.#. => #",
	              ".#.## => #",
	              ".##.. => #",
	              ".#### => #",
	              "#.#.# => #",
	              "#.### => #",
	              "##.#. => #",
	              "##.## => #",
	              "###.. => #",
	              "###.# => #",
	              "####. => #"]

	state = TEST_INPUT[0]
	generations = [Generation(s) for s in TEST_INPUT[1:]]

	state, offset = grow(state, generations, 20)

	assert (sum_plants(state, offset) == 325)

	return sum_plants(state, offset)


def first():
	state = INPUT[0]
	generations = [Generation(s) for s in INPUT[1:]]

	state, offset = grow(state, generations, 20)

	return sum_plants(state, offset)


def second():
	state = INPUT[0]
	generations = [Generation(s) for s in INPUT[1:]]

	state, offset = grow(state, generations, 200)

	# When analyzing the state, one can see that the pattern of pots with plants starts repeating at generation 195,
	# but the offset is still decreasing (that is, the pattern with pots that have plants stays the same but
	# is moving toward the right). Per generation the sum then increases with 45 points
	s = sum_plants(state, offset)

	return s + (50000000000 - 200) * 45


if __name__ == "__main__":
	print("Sum of plants after 20 generations: {0}".format(test()))

	print("Sum of plants after 20 generations: {0}".format(first()))
	print("Sum of plants after 50 billion generations: {0}".format(second()))
