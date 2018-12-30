import queue

INPUT = ["################################",
         "#####################...########",
         "###################....G########",
         "###################....#########",
         "#######.##########......########",
         "#######G#########........#######",
         "#######G#######.G.........######",
         "#######.######..G.........######",
         "#######.......##.G...G.G..######",
         "########..##..#....G......G#####",
         "############...#.....G.....#####",
         "#...#######..........G.#...#####",
         "#...#######...#####G......######",
         "##...######..#######G.....#.##.#",
         "###.G.#####.#########G.........#",
         "###G..#####.#########.......#.E#",
         "###..######.#########..........#",
         "###.......#.#########.....E..E.#",
         "#####G...#..#########.......#..#",
         "####.G.#.#...#######.....G.....#",
         "########......#####...........##",
         "###########..................###",
         "##########.................#####",
         "##########.................#####",
         "############..E.........E.....##",
         "############.........E........##",
         "###############.#............E##",
         "##################...E..E..##.##",
         "####################.#E..####.##",
         "################.....######...##",
         "#################.#..###########",
         "################################"]


class Location:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def above(self):
		return Location(self.x, self.y - 1)

	def left_of(self):
		return Location(self.x - 1, self.y)

	def right_of(self):
		return Location(self.x + 1, self.y)

	def below(self):
		return Location(self.x, self.y + 1)

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	def __hash__(self):
		return hash((self.y << 16) | self.x)


class BreadthFirst:
	def __init__(self, map):
		self.map = map

	def __getitem__(self, location):
		return self.map[location.y][location.x]

	def neighbors(self, location):
		n = list()
		if self[location.above()] != "#":
			n.append(location.above())
		if self[location.right_of()] != "#":
			n.append(location.right_of())
		if self[location.below()] != "#":
			n.append(location.below())
		if self[location.left_of()] != "#":
			n.append(location.left_of())

		return n

	def calculate_map(self, start, target=None):
		frontier = queue.Queue()
		frontier.put(start)

		map = dict()
		map[start] = None

		while not frontier.empty():
			current = frontier.get()

			# Bail out early if target (if any) was found
			if target is not None and current == target:
				break

			for n in self.neighbors(current):
				if n not in map:
					frontier.put(n)
					map[n] = current

		return map

	def get_path(self, map, start, target):
		current = target

		path = []
		while current != start:
			path.append(current)
			current = map[current]
		path.append(start)  # optional
		path.reverse()  # optional

		return path


class Unit:
	def __init__(self, x, y):
		self.hp = 200
		self.location = Location(x, y)
		self.targets = list()

	def targets(self, map):
		pass


def test():
	pass


def first():
	return 0


def second():
	return 0


if __name__ == "__main__":
	test()
	print("Blaat: {0}".format(first()))
	print("Blaat: {0}".format(second()))
