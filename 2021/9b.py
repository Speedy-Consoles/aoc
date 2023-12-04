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

DIRECTIONS = [Vec(1, 0), Vec(0, 1), Vec(-1, 0), Vec(0, -1)]

height_map = [[int(c) for c in line] for line in sys.stdin.read().splitlines()]
width = len(height_map[0])
depth = len(height_map)

basin_sizes = []
seen = set()
for y, line in enumerate(height_map):
	for x, height in enumerate(line):
		start_position = Vec(x, y)
		if height == 9 or start_position in seen:
			continue

		fringe = [start_position]
		seen.add(start_position)
		basin_size = 1
		while len(fringe) > 0:
			position = fringe.pop()
			for direction in DIRECTIONS:
				next_position = position + direction

				if next_position in seen:
					continue

				in_bounds = (
					    next_position.x >= 0
					and next_position.x < width
					and next_position.y >= 0
					and next_position.y < depth
				)
				if not in_bounds:
					continue

				next_height = height_map[next_position.y][next_position.x]
				if next_height == 9:
					continue

				fringe.append(next_position)
				seen.add(next_position)
				basin_size += 1
		basin_sizes.append(basin_size)

sorted_basin_sizes = sorted(basin_sizes)
print(sorted_basin_sizes[-1] * sorted_basin_sizes[-2] * sorted_basin_sizes[-3])
