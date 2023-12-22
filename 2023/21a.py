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

	def in_bounds(self, width, height):
		return self.x >= 0 and self.x < width and self.y >= 0 and self.y < height

	def __str__(self):
		return '({}, {})'.format(self.x, self.y)

	def __repr__(self):
		return 'Vec({}, {})'.format(self.x, self.y)

def get_num_reachable(garden, start, num_steps):
	DIRECTIONS = [
		Vec( 1,  0),
		Vec( 0,  1),
		Vec(-1,  0),
		Vec( 0, -1),
	]

	width = len(garden[0])
	height = len(garden)

	fringe = deque([start])
	distances = {start: 0}
	while len(fringe) > 0:
		plot = fringe.popleft()
		distance = distances[plot]
		if distance == num_steps:
			continue
		for direction in DIRECTIONS:
			new_plot = plot + direction
			if not new_plot.in_bounds(width, height):
				continue
			if garden[new_plot.y][new_plot.x] == '#':
				continue
			if new_plot in distances:
				continue
			fringe.append(new_plot)
			distances[new_plot] = distance + 1

	return sum((v.x + v.y + num_steps + 1) % 2 for v in distances)


garden = sys.stdin.read().splitlines()
width = len(garden[0])
height = len(garden)

start = next(Vec(x, y) for y in range(height) for x in range(width) if garden[y][x] == 'S')

print(get_num_reachable(garden, start, 64))

