import sys
import re

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

def in_bounds(position, left, right, top, bottom):
	return (
		position.x >= left - 1
		and position.x < right + 1
		and position.y >= top - 1
		and position.y < bottom + 1
	)

DIRECTIONS = {
	'R': Vec( 1,  0),
	'D': Vec( 0,  1),
	'L': Vec(-1,  0),
	'U': Vec( 0, -1),
}
PATTERN = re.compile(r'^(R|D|L|U) (\d+) \(#[0-9a-f]{6}\)$')

position = Vec(0, 0)
trench = {position}
for line in sys.stdin.read().splitlines():
	direction_string, count_string = PATTERN.match(line).groups()
	direction = DIRECTIONS[direction_string]
	count = int(count_string)

	for i in range(count):
		position += direction
		trench.add(position)

left = min(v.x for v in trench)
right = max(v.x for v in trench) + 1
top = min(v.y for v in trench)
bottom = max(v.y for v in trench) + 1

start = Vec(left - 1, top - 1)
fringe = [start]
seen = {start}
while len(fringe) > 0:
	position = fringe.pop()
	for direction in DIRECTIONS.values():
		new_position = position + direction
		if not in_bounds(new_position, left, right, top, bottom):
			continue
		if new_position in seen:
			continue
		if new_position in trench:
			continue
		fringe.append(new_position)
		seen.add(new_position)

print((right - left + 2) * (bottom - top + 2) - len(seen))
