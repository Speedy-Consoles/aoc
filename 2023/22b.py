import sys
import re
import copy
from collections import defaultdict

class Vec(object):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __hash__(self):
		return hash((self.x, self.y, self.z))

	def __eq__(self, other):
		return isinstance(other, Vec) and other.x == self.x and other.y == self.y and other.z == self.z

	def __add__(self, other):
		return Vec(self.x + other.x, self.y + other.y, self.z + other.z)

	def __sub__(self, other):
		return Vec(self.x - other.x, self.y - other.y, self.z - other.z)

	def __mul__(self, factor):
		return Vec(self.x * factor, self.y * factor, self.z * factor)

	def __floordiv__(self, divisor):
		return Vec(self.x // divisor, self.y // divisor, self.z // divisor)

	def __abs__(self):
		return abs(self.x) + abs(self.y) + abs(self.z)

	def man_dist(self, other):
		return abs(other - self)

	def __str__(self):
		return '({}, {}, {})'.format(self.x, self.y, self.z)

	def __repr__(self):
		return 'Vec({}, {}, {})'.format(self.x, self.y, self.z)

PATTERN = re.compile(r'^(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)$')

def parse_brick(s):
	x1, y1, z1, x2, y2, z2 = map(int, PATTERN.match(s).groups())
	return Vec(x1, y1, z1), Vec(x2, y2, z2)


bricks = sorted(map(parse_brick, sys.stdin.read().splitlines()), key=lambda v: v[0].z)

assert(a >= b for brick in bricks for a, b in zip(*brick))

width = max(v.x for brick in bricks for v in brick) + 1
depth = max(v.y for brick in bricks for v in brick) + 1
height = max(v.z for brick in bricks for v in brick) + 1

pile = [[[None] * width for _ in range(depth)] for _ in range(height)]
column_heights = [[0] * width for _ in range(depth)]

belows = defaultdict(set)
aboves = defaultdict(set)
for brick_id, brick in enumerate(bricks):
	diff = brick[1] - brick[0]
	diff_length = abs(diff)
	direction = diff // diff_length if diff_length > 0 else Vec(0, 0, 0)
	length = diff_length + 1

	position = copy.deepcopy(brick[0])
	max_column_height = 0
	for i in range(length):
		max_column_height = max(max_column_height, column_heights[position.y][position.x])
		position += direction

	position = copy.deepcopy(brick[0])
	position.z = max_column_height
	for i in range(length):
		if position.z > 0:
			below = pile[position.z - 1][position.y][position.x]
			if below is not None and below != brick_id:
				aboves[below].add(brick_id)
				belows[brick_id].add(below)
		pile[position.z][position.y][position.x] = brick_id
		column_heights[position.y][position.x] = position.z + 1
		position += direction

result = 0
for brick_id in range(len(bricks)):
	removed = {brick_id}
	fringe = [brick_id]
	while len(fringe) > 0:
		current = fringe.pop()
		for above in aboves[current]:
			if all(below in removed for below in belows[above]):
				fringe.append(above)
				removed.add(above)
	result += len(removed) - 1

print(result)
