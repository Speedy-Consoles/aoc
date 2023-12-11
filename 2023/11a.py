import sys

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

image = sys.stdin.read().splitlines()
column_empty = [all(row[x] == '.' for row in image) for x in range(len(image[0]))]
galaxies = []
y = 0
for row in image:
	x = 0
	row_empty = True
	for i, c in enumerate(row):
		if c == '#':
			galaxies.append(Vec(x, y))
			row_empty = False
		if column_empty[i]:
			x += 1
		x += 1
	if row_empty:
		y += 1
	y += 1

print(sum(v1.man_dist(v2) for i, v1 in enumerate(galaxies) for v2 in galaxies[i + 1:]))
