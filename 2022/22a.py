import sys
import re

PATTERN = re.compile('(\\d+|R|L)')
class Vec(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, other):
		return type(other) == Vec and self.x == other.x and self.y == other.y

	def __hash__(self):
		return hash((self.x, self.y))

	def __add__(self, other):
		return Vec(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vec(self.x - other.x, self.y - other.y)

	def __str__(self):
		return '({}, {})'.format(self.x, self.y)


def print_map(monkey_map, pos, direction):
	width = max(monkey_map, key=lambda v: v.x).x + 1
	height = max(monkey_map, key=lambda v: v.y).y + 1
	for y in range(height):
		for x in range(width):
			p = Vec(x, y)
			if p == pos:
				c = ['>', 'v', '<', '^'][direction]
			elif p not in monkey_map:
				c = ' '
			else:
				c = monkey_map[p]
			print(c, end='')
		print()

DIRS = (Vec(1, 0), Vec(0, 1), Vec(-1, 0), Vec(0, -1))


map_string, instructions_string = sys.stdin.read().split('\n\n')
monkey_map = {}
pos = None
for y, line in enumerate(map_string.splitlines()):
	for x, c in enumerate(line):
		if c != ' ':
			if y == 0 and pos is None:
				pos = Vec(x, y)
			monkey_map[Vec(x, y)] = c

instructions = (int(s) if s not in ('R', 'L') else s for s in PATTERN.findall(instructions_string))

d = 0
for instruction in instructions:
	if instruction == 'R':
		d = (d + 1) % 4
	elif instruction == 'L':
		d = (d - 1) % 4
	else:
		for i in range(instruction):
			new_pos = pos + DIRS[d]
			if new_pos not in monkey_map:
				p = pos
				while p in monkey_map:
					p -= DIRS[d]
				new_pos = p + DIRS[d]
			if monkey_map[new_pos] == '.':
				pos = new_pos
			else:
				break;
	#print_map(monkey_map, pos, d)
	#print()

print((pos.y + 1) * 1000 + (pos.x + 1) * 4 + d)
