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

INPUT = ["#..#.#..##......###...###",
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


class Plant:
	def __init__(self, s):
		self.match = s[0:5]
		self.plant = s[9]

	def apply(self, next_state, current_state):
		# Match self.match at start of current_state (assume infinite "." at start) when self.match starts with "." or ".."
		# Match self.match in between
		# Match self.match at end of current_state (assume infinite "." at end) when self.match ends with "." or ".."

		prepend = []
		append = []

		state_str = ".." + "".join(current_state) + ".."
		o = 0;
		while o != -1:
			o = state_str.find(self.match, o)
			if o != -1:
				if o < 2:
					prepend.append(self.plant)
				elif o >= len(current_state) - 2:
					append.append(self.plant)
				else:
					next_state[o + 2] = self.plant
				o += 1

		return prepend + next_state + append


def test():
	current_state = list(INPUT[0])

	plants = [Plant(s) for s in INPUT[1:]]
	for s in range(21):

		print("{0:02d}:  {1}".format(s, "".join(current_state)))

		next_state = ["." for _ in range(len(current_state))]

		for plant in plants:
			next_state = plant.apply(next_state, current_state)

		current_state = next_state


if __name__ == "__main__":
	test()

	print("Blaat")

	print("Blaat")
