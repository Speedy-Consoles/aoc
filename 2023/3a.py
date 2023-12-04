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


DIRS = [
	Vec( 1,  0),
	Vec( 1,  1),
	Vec( 0,  1),
	Vec(-1,  1),
	Vec(-1,  0),
	Vec(-1, -1),
	Vec( 0, -1),
	Vec( 1, -1),
]

def get_character(p, schematics):
	return schematics[p.y][p.x]

def is_symbol(c):
	return not c.isdigit() and c != '.'

def in_range(p, start, end):
	return p.x >= start.x and p.y >= start.y and p.x < end.x and p.y < end.y

def neighbors(p, schematics):
	width = len(schematics[0])
	height = len(schematics)
	for v in DIRS:
		np = p + v
		if in_range(p + v, Vec(0, 0), Vec(width, height)):
			yield np

def touches_symbol(p, schematics):
	return any(is_symbol(get_character(np, schematics)) for np in neighbors(p, schematics))

def handle_number():
	global digit_buffer, number_sum, number_active
	if number_active:
		number_sum += int(digit_buffer)
	digit_buffer = ''
	number_active = False

schematics = sys.stdin.read().splitlines()
width = len(schematics[0])
height = len(schematics)

number_active = False
digit_buffer = ''
number_sum = 0
for y in range(height):
	for x in range(width):
		p = Vec(x, y)
		c = get_character(p, schematics)
		if c.isdigit():
			digit_buffer += c
			number_active = number_active or touches_symbol(p, schematics)
		else:
			handle_number()
	handle_number()

print(number_sum)
