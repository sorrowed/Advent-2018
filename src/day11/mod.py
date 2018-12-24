import math

INPUT = 3463
WIDTH = 300
HEIGHT = 300


class FuelCell:
	def __init__(self, serial, x, y):
		self.serial = serial
		self.x = x
		self.y = y
		self.power = self.power_level()

	@classmethod
	def keep_thousand(cls, k):
		return int((k % 1000) / 100)

	def rack_id(self):
		return self.x + 10

	def power_level(self):
		return FuelCell.keep_thousand((self.rack_id() * self.y + self.serial) * self.rack_id()) - 5

	def __str__(self):
		return "({0:3d},{1:3d})".format(self.x, self.y)


class FuelCellGrid:
	def __init__(self, cells):
		self.cells = cells

	def power_level(self):
		return sum(cell.power for cell in self.cells)


def create_power_array(width, height):
	array = [[None] * width for _ in range(height)]

	for y in range(0, height):
		for x in range(0, width):
			array[x][y] = FuelCell(INPUT, x + 1, y + 1)

	return array


def test():
	assert (FuelCell(8, 3, 5).power == 4)
	assert (FuelCell(57, 122, 79).power == -5)
	assert (FuelCell(39, 217, 196).power == 0)
	assert (FuelCell(71, 101, 153).power == 4)


def summed_area_table(array, width, height):
	table = [[0] * width for _ in range(height)]
	for y in range(0, height):
		for x in range(0, width):
			grid = FuelCellGrid([array[xx][yy] for yy in range(0, y) for xx in range(0, x)])
			table[x][y] = grid.power_level()
	return table


def summed_area_table_sum(table, tl, br):
	return table[br[0]][br[1]] + \
	       table[tl[0]][tl[1]] - \
	       table[br[0]][tl[1]] - \
	       table[tl[0]][br[1]]


def first():
	array = create_power_array(WIDTH, HEIGHT)

	g = None
	for y in range(0, HEIGHT - 3):
		for x in range(0, WIDTH - 3):
			grid = FuelCellGrid([array[xx][yy] for yy in range(y, y + 3) for xx in range(x, x + 3)])
			if g is None or grid.power_level() > g.power_level():
				g = grid

	return g.cells[0]


def second():
	array = create_power_array(WIDTH, HEIGHT)

	g = None
	for s in range(1, 300 + 1):
		for y in range(0, HEIGHT - s):
			for x in range(0, WIDTH - s):
				grid = FuelCellGrid([array[xx][yy] for yy in range(y, y + s) for xx in range(x, x + s)])
				if g is None or grid.power_level() > g.power_level():
					g = grid

	return g.cells[0], int(math.sqrt(len(g.cells)))


def second_sat():
	sat = summed_area_table(create_power_array(WIDTH, HEIGHT), WIDTH, HEIGHT)

	g = None
	for s in range(1, HEIGHT + 1):
		for y in range(0, HEIGHT - s + 1):
			for x in range(0, WIDTH - s + 1):
				summed = summed_area_table_sum(sat, (x, y), (x + s - 1, y + s - 1))
				if g is None or summed > g[2]:
					g = (x + 1, y + 1), s, summed

	return g


if __name__ == "__main__":
	test()
	r = first()
	print("Coordinates of max power cell :{0},{1}".format(r.x, r.y))

	r = second()
	print("Coordinates and size of max power cell :{0},{1}".format(r[0], r[1]))
