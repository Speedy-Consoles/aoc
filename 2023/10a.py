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

def get_connected_neighbors(p, pipes):
	for v in DIRS:
		np = p + v
		if in_range(np, pipes):
			pipe = pipes[np.y][np.x]
			if pipe != '.' and p in (np + DIRS[d] for d in NEIGHBOR_DIRS[pipe]):
				yield np

pipes = sys.stdin.read().splitlines()

start = next(Vec(x, y) for y in range(len(pipes)) for x in range(len(pipes[0])) if pipes[y][x] == 'S')
first_neighbor = next(get_connected_neighbors(start, pipes))

fringe = deque([first_neighbor])
loop = {start, first_neighbor}

while len(fringe) > 0:
	p = fringe.popleft()
	pipe = pipes[p.y][p.x]
	for d in NEIGHBOR_DIRS[pipe]:
		np = p + DIRS[d]
		if np not in loop:
			fringe.append(np)
			loop.add(np)

print(len(loop) // 2)

