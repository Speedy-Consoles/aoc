import sys
import functools


@functools.total_ordering
class Vec:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __add__(self, other):
		return Vec(self.x + other.x, self.y + other.y)

	def __eq__(self, other):
		if type(self) != type(other):
			return False
		return self.x == other.x and self.y == other.y

	def __lt__(self, other):
		if type(self) != type(other):
			return NotImplemented
		return self.y < other.y or (self.y == other.y and self.y < other.y)

	def __hash__(self):
		return hash((self.x, self.y))

	def __str__(self):
		return '({}, {})'.format(self.x, self.y)

	def __repr__(self):
		return 'Vec({}, {})'.format(self.x, self.y)


DIRECTIONS = [Vec(0, -1), Vec(-1, 0), Vec(1, 0), Vec(0, 1)]

grid = [[int(x) for x in line] for line in sys.stdin.read().splitlines()]
width = len(grid[0])
height = len(grid)

fringe = {Vec(0, 0)}
partial_risks = {Vec(0, 0): 0}

while len(fringe) > 0:
	position = min(fringe, key=lambda x: partial_risks[x])
	fringe.remove(position)
	for direction in DIRECTIONS:
		neighbor = position + direction
		if neighbor in partial_risks:
			continue
		if neighbor.x < 0 or neighbor.x >= width or neighbor.y < 0 or neighbor.y >= height:
			continue
		partial_risk = partial_risks[position] + grid[neighbor.y][neighbor.x]
		if neighbor.x == width - 1 and neighbor.y == height - 1:
			print(partial_risk)
			sys.exit(0)
		partial_risks[neighbor] = partial_risk
		fringe.add(neighbor)
sys.exit(1)
