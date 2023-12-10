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

	def __abs__(self):
		return abs(self.x) + abs(self.y)

	def man_dist(self, other):
		return abs(other - self)

	def __str__(self):
		return '({}, {})'.format(self.x, self.y)

	def __repr__(self):
		return 'Vec({}, {})'.format(self.x, self.y)

DIRS = [
	Vec( 1,  0),
	Vec( 0,  1),
	Vec(-1,  0),
	Vec( 0, -1),
]

NEIGHBOR_DIRS = {
	'|': (1, 3),
	'-': (0, 2),
	'L': (0, 3),
	'J': (3, 2),
	'7': (2, 1),
	'F': (1, 0),
}

def in_range(p, pipes):
	return p.x >= 0 and p.y >= 0 and p.x < len(pipes[0]) and p.y < len(pipes)

def get_neighbors(p):
	return (p + v for v in DIRS)

def get_connected_neighbors(p, pipes):
	for np in get_neighbors(p):
		if in_range(np, pipes):
			pipe = pipes[np.y][np.x]
			if pipe != '.' and p in (np + DIRS[d] for d in NEIGHBOR_DIRS[pipe]):
				yield np

def flood(p, loop, pipes):
	if not in_range(p, pipes):
		return set(), True

	fringe = deque([p])
	visited = set(loop)
	flooded = {p}
	outside = False
	while len(fringe) > 0:
		for np in get_neighbors(fringe.popleft()):
			if not in_range(np, pipes):
				outside = True
			elif np not in visited and np not in flooded:
				fringe.append(np)
				visited.add(np)
				flooded.add(np)
	return flooded, outside

def index_of_second(value, iterable):
	return next(i for i, (_, second) in enumerate(iterable) if second == value)

pipes = sys.stdin.read().splitlines()

start = next(Vec(x, y) for y in range(len(pipes)) for x in range(len(pipes[0])) if pipes[y][x] == 'S')
first_neighbor = next(get_connected_neighbors(start, pipes))

fringe = deque([first_neighbor])
loop = {start: 0, first_neighbor: 1}

while len(fringe) > 0:
	p = fringe.popleft()
	pipe = pipes[p.y][p.x]
	for d in NEIGHBOR_DIRS[pipe]:
		np = p + DIRS[d]
		if np not in loop:
			fringe.append(np)
			loop[np] = len(loop)

loop_size = len(loop)

flood_areas = [set(), set()]
outside_index = None
for p, index in loop.items():
	neighbors = [(np, loop.get(np)) for np in get_neighbors(p)]

	prev_loop_index = (index + loop_size - 1) % loop_size
	next_loop_index = (index + 1) % loop_size

	prev_neighbor_index = index_of_second(prev_loop_index, neighbors)
	rotated_neighbors = neighbors[prev_neighbor_index:] + neighbors[:prev_neighbor_index]

	flood_area_index = 0
	for np, neighbor_loop_index in rotated_neighbors:
		if neighbor_loop_index is None:
			if np not in flood_areas[0] and np not in flood_areas[1]:
				flood_area, outside = flood(np, loop, pipes)
				flood_areas[flood_area_index] |= flood_area
				if outside:
					outside_index = flood_area_index
		elif neighbor_loop_index == next_loop_index:
			flood_area_index = 1

print(len(flood_areas[1 - outside_index]))
