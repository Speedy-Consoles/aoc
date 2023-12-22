import sys
from collections import deque

class Vec(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __hash__(self):
		return hash((self.x, self.y))

	def __eq__(self, other):
		return isinstance(other, Vec) and other.x == self.x and other.y == self.y

	def __add__(self, other):
		return Vec(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vec(self.x - other.x, self.y - other.y)

	def __mul__(self, factor):
		return Vec(self.x * factor, self.y * factor)

	def __abs__(self):
		return abs(self.x) + abs(self.y)

	def man_dist(self, other):
		return abs(other - self)

	def in_bounds(self, width, height):
		return self.x >= 0 and self.x < width and self.y >= 0 and self.y < height

	def __str__(self):
		return '({}, {})'.format(self.x, self.y)

	def __repr__(self):
		return 'Vec({}, {})'.format(self.x, self.y)

def get_reachable(garden, start):
	DIRECTIONS = [
		Vec( 1,  0),
		Vec( 0,  1),
		Vec(-1,  0),
		Vec( 0, -1),
	]

	width = len(garden[0])
	height = len(garden)

	fringe = deque([start])
	seen = {start}
	while len(fringe) > 0:
		plot = fringe.popleft()
		for direction in DIRECTIONS:
			new_plot = plot + direction
			if not new_plot.in_bounds(width, height):
				continue
			if garden[new_plot.y][new_plot.x] == '#':
				continue
			if new_plot in seen:
				continue
			fringe.append(new_plot)
			seen.add(new_plot)

	return seen

'''
def should_be_free(position, size):
	half_size = size // 2
	origin = Vec(half_size, half_size)
	components = (position.x, position.y)
	line_offsets = (0, half_size, size - 1)
	diagonal_distance = abs(position.man_dist(origin) - half_size)
	return any(v in components for v in line_offsets) or diagonal_distance < 4
'''


NUM_STEPS = 26501365

garden = sys.stdin.read().splitlines()
size = len(garden)
half_size = size // 2
origin = Vec(half_size, half_size)

'''
assert(len(garden[0]) == size)
assert(size % 2 == 1)
assert(garden[half_size][half_size] == 'S')
assert(NUM_STEPS % size == half_size)
assert(all(garden[y][x] != '#' for y in range(size) for x in range(size) if should_be_free(Vec(x, y), size)))
'''

n = (NUM_STEPS - half_size) // size
parity = NUM_STEPS % 2
garden_parities = [(n + parity + i) % 2 for i in range(2)]

num_cells = (NUM_STEPS + 1)**2

reachable = get_reachable(garden, origin)
stones = [
	[Vec(x, y) for y in range(size) for x in range(size) if Vec(x, y) not in reachable and (x + y) % 2 == i]
	for i in range(2)
]

num_stones = [len(s) for s in stones]
num_corner_stones = [sum(int(abs(stone - origin) > half_size) for stone in s) for s in stones]

base_num_stones = sum((n + 1 - i)**2 * num_stones[garden_parities[i]] for i in range(2))
num_bulge_stones = num_corner_stones[garden_parities[0]] * (n + 1)
num_dent_stones = num_corner_stones[garden_parities[1]] * n

print(num_cells - base_num_stones + num_bulge_stones - num_dent_stones)
