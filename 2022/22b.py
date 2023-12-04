import sys
import re
from numbers import Number
from collections import deque

SIDE_LENGTH = 50
#SIDE_LENGTH = 4

PATTERN = re.compile('(\\d+|R|L)')

class Vec(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __eq__(self, other):
		return isinstance(other, Vec) and self.x == other.x and self.y == other.y

	def __hash__(self):
		return hash((self.x, self.y))

	def __add__(self, other):
		return Vec(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vec(self.x - other.x, self.y - other.y)

	def __mul__(self, other):
		if not isinstance(other, Number):
			raise ValueError('Can only multiply by numbers')
		return Vec(self.x * other, self.y * other)

	def __truediv__(self, other):
		if not isinstance(other, Number):
			raise ValueError('Can only divide by numbers')
		return Vec(self.x / other, self.y / other)

	def __floordiv__(self, other):
		if not isinstance(other, Number):
			raise ValueError('Can only divide by numbers')
		return Vec(self.x // other, self.y // other)

	def __mod__(self, other):
		if not isinstance(other, Number):
			raise ValueError('Can only divide by numbers')
		return Vec(self.x % other, self.y % other)

	def __str__(self):
		return '({}, {})'.format(self.x, self.y)

	def __repr__(self):
		return 'Vec({}, {})'.format(self.x, self.y)

def print_map(monkey_map, pos, direction):
	width = max(monkey_map, key=lambda v: v.x).x + 1
	height = max(monkey_map, key=lambda v: v.y).y + 1
	for y in range(height):
		for x in range(width):
			p = Vec(x, y)
			if p == pos:
				c = ('>', 'v', '<', '^')[direction]
			elif p not in monkey_map:
				c = ' '
			else:
				c = monkey_map[p]
			print(c, end='')
		print()

def rotate_position(local_position, steps):
	for i in range(steps % 4):
		local_position = Vec(SIDE_LENGTH - local_position.y - 1, local_position.x)
	return local_position

def wrap(monkey_map, position, direction_index):
	sector_position = position // SIDE_LENGTH
	target_local_position = (position + DIRS[direction_index]) % SIDE_LENGTH
	sector_direction_index = direction_index
	target_direction = direction_index
	sector_distance = 1
	visited = {sector_position}
	fringe = deque([(sector_position, sector_direction_index, sector_distance, target_local_position, target_direction)])
	while len(fringe) > 0:
		current_sp, current_sdi, current_sd, current_tlp, current_tdi = fringe.popleft()
		for d in range(4):
			next_sp = current_sp + DIRS[d]
			if (next_sp * SIDE_LENGTH) in monkey_map and next_sp not in visited:
				direction_index_diff = (d - current_sdi) % 4
				if current_sd == 1:
					if direction_index_diff == 0:
						return current_tlp + next_sp * SIDE_LENGTH, current_tdi
					elif direction_index_diff in (1, 3):
						next_sd = 1
						next_tlp = rotate_position(current_tlp, direction_index_diff)
						next_tdi = (current_tdi + direction_index_diff) % 4
					else:
						next_sd = 2
						next_tlp = current_tlp
						next_tdi = current_tdi
					next_sdi = current_sdi
				else:
					next_tlp = rotate_position(current_tlp, 2 * direction_index_diff)
					next_tdi = (current_tdi + 2 * direction_index_diff) % 4
					next_sdi = d
					next_sd = 1
				visited.add(next_sp)
				fringe.append((next_sp, next_sdi, next_sd, next_tlp, next_tdi))

DIRS = (Vec(1, 0), Vec(0, 1), Vec(-1, 0), Vec(0, -1))


map_string, instructions_string = sys.stdin.read().split('\n\n')
monkey_map = {}
position = None
for y, line in enumerate(map_string.splitlines()):
	for x, c in enumerate(line):
		if c != ' ':
			if y == 0 and position is None:
				position = Vec(x, y)
			monkey_map[Vec(x, y)] = c

instructions = (int(s) if s not in ('R', 'L') else s for s in PATTERN.findall(instructions_string))

direction_index = 0
for instruction in instructions:
	if instruction == 'R':
		direction_index = (direction_index + 1) % 4
	elif instruction == 'L':
		direction_index = (direction_index + 3) % 4
	else:
		for i in range(instruction):
			new_position = position + DIRS[direction_index]
			new_direction_index = direction_index
			if new_position not in monkey_map:
				new_position, new_direction_index = wrap(monkey_map, position, direction_index)
			if monkey_map[new_position] == '.':
				position = new_position
				direction_index = new_direction_index
			else:
				break;
	#print_map(monkey_map, position, direction_index)
	#print()

print((position.y + 1) * 1000 + (position.x + 1) * 4 + direction_index)
