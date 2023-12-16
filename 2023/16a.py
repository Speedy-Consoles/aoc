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

DIRECTIONS = [
	Vec( 1,  0),
	Vec( 0,  1),
	Vec(-1,  0),
	Vec( 0, -1),
]

grid = sys.stdin.read().splitlines()

beams = [(Vec(0, 0), 0)]
energized_tiles = {}

while len(beams) > 0:
	position, direction_index = beams.pop()

	if position.x < 0 or position.x >= len(grid[0]) or position.y < 0 or position.y >= len(grid):
		continue

	tile = grid[position.y][position.x]

	direction_indices = energized_tiles.get(position)
	if direction_indices is None:
		energized_tiles[position] = {direction_index}
	elif direction_index not in direction_indices:
		direction_indices.add(direction_index)
	else:
		continue

	if tile in ('/', '\\'):
		new_direction_index = direction_index ^ 1
		if tile == '/':
			new_direction_index ^= 2
		beams.append((position + DIRECTIONS[new_direction_index], new_direction_index))
	elif tile in ('|', '-') and direction_index % 2 != int(tile == '|'):
		bit = int(tile == '|')
		if direction_index % 2 != bit:
			beams.append((position + DIRECTIONS[bit], bit))
			beams.append((position + DIRECTIONS[2 + bit], 2 + bit))
	else:
		beams.append((position + DIRECTIONS[direction_index], direction_index))

print(len(energized_tiles))
