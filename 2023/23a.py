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

SLOPE_DIRECTIONS = {
	'>': 0,
	'v': 1,
	'<': 2,
	'^': 3,
}

def find_longest(grid, start, visited):
	width = len(grid[0])
	height = len(grid)

	length = 0
	position = start
	while True:
		if position.y == height - 1:
			return length

		content = grid[position.y][position.x]
		if content == '.':
			directions = DIRECTIONS
		else:
			directions = [DIRECTIONS[SLOPE_DIRECTIONS[content]]]

		next_positions = []
		for direction in directions:
			next_position = position + direction
			if next_position.y < 0:
				continue
			if grid[next_position.y][next_position.x] == '#':
				continue
			if next_position in visited:
				continue
			next_positions.append(next_position)

		if len(next_positions) == 0:
			return None

		length += 1
		if len(next_positions) == 1:
			position = next_positions[0]
			visited.add(position)
		else:
			lengths = list(filter(
				lambda x: x is not None,
				(find_longest(grid, next_position, visited | {next_position}) for next_position in next_positions)
			))
			if len(lengths) == 0:
				return None
			else:
				return length + max(lengths)

grid = sys.stdin.read().splitlines()
width = len(grid[0])
height = len(grid)

start = Vec(next(x for x in range(width) if grid[0][x] == '.'), 0)

print(find_longest(grid, start, set()))

