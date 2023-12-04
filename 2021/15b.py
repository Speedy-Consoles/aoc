import sys
import functools
import heapq

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

input_grid = [[int(x) for x in line] for line in sys.stdin.read().splitlines()]
input_width = len(input_grid[0])
input_height = len(input_grid)

width = input_width * 5
height = input_height * 5

grid = [[None for j in range(width)] for i in range(height)]
for y in range(height):
	for x in range(width):
		increment = x // input_width + y // input_height
		grid[y][x] = (((input_grid[y % input_height][x % input_width]) - 1 + increment) % 9) + 1

fringe = [(0, Vec(0, 0))]
seen = {Vec(0, 0)}

while len(fringe) > 0:
	partial_risk, position = heapq.heappop(fringe)
	for direction in DIRECTIONS:
		neighbor = position + direction
		if neighbor in seen:
			continue
		if neighbor.x < 0 or neighbor.x >= width or neighbor.y < 0 or neighbor.y >= height:
			continue
		neighbor_partial_risk = partial_risk + grid[neighbor.y][neighbor.x]
		if neighbor.x == width - 1 and neighbor.y == height - 1:
			print(neighbor_partial_risk)
			sys.exit(0)
		heapq.heappush(fringe, (neighbor_partial_risk, neighbor))
		seen.add(neighbor)
sys.exit(1)
