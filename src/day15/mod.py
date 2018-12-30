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


class Map:
	def __init__(self, map):
		self.map, self.units = self.process(map)

	def __getitem__(self, location):
		return self.map[location.y][location.x]

	def process(self, map):
		m, units = list(), list()

		for y in range(len(map)):
			line = list()
			for x in range(len(map[y])):
				if map[y][x] == "#" or map[y][x] == ".":
					line.append(map[y][x])
				elif map[y][x] == "G" or map[y][x] == "E":
					units.append(Unit(map[y][x], x, y))
					line.append(".")

			m.append(line)

		return m, units

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
	def __init__(self, map, start):
		self.start = start
		self.search_map = self.calculate_search_map(map, start)

	@staticmethod
	def calculate_search_map(map, start, target=None):
		frontier = queue.Queue()
		frontier.put(start)

		path_map = dict()
		path_map[start] = None

		while not frontier.empty():
			current = frontier.get()

			# Bail out early if target (if any) was found
			if target is not None and current == target:
				break

			for n in map.neighbors(current):
				if n not in path_map:
					frontier.put(n)
					path_map[n] = current

		return path_map

	def get_path(self, target):
		current = target

		path = []
		while current != self.start:
			path.append(current)
			current = self.search_map[current]
		path.append(self.start)  # optional
		path.reverse()  # optional

		return path


class Unit:
	def __init__(self, type, x, y):
		self.hp = 200
		self.type = type
		self.location = Location(x, y)


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
