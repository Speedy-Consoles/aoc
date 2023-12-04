import sys
from collections import defaultdict

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

DIR_SETS = [
	(
		Vec(-1, -1),
		Vec(0, -1),
		Vec(1, -1),
	), (
		Vec(1, 1),
		Vec(0, 1),
		Vec(-1, 1),
	), (
		Vec(-1, 1),
		Vec(-1, 0),
		Vec(-1, -1),
	), (
		Vec(1, -1),
		Vec(1, 0),
		Vec(1, 1),
	)
]

DIRS = [
	Vec(0, -1),
	Vec(0, 1),
	Vec(-1, 0),
	Vec(1, 0),
]

def print_grove(elves, marks):
	start_x = min(elves | set(marks.keys()), key=lambda e: e.x).x
	start_y = min(elves | set(marks.keys()), key=lambda e: e.y).y
	end_x = max(elves | set(marks.keys()), key=lambda e: e.x).x + 1
	end_y = max(elves | set(marks.keys()), key=lambda e: e.y).y + 1

	for y in range(start_y, end_y):
		for x in range(start_x, end_x):
			p = Vec(x, y)
			if p in elves:
				c = '#'
			elif p in marks:
				c = str(marks[p])
			else:
				c = '.'
			print(c, end='')
		print()

elves = {Vec(x, y) for y, line in enumerate(sys.stdin.read().splitlines()) for x, c in enumerate(line) if c == '#'}

start_dir_index = 0
for r in range(10):
	marks = defaultdict(int)
	propositions = {}
	for e in elves:
		proposition = None
		found = False
		for i in range(4):
			d = (start_dir_index + i) % 4
			if all((e + dir) not in elves for dir in DIR_SETS[d]):
				if proposition is None:
					proposition = e + DIRS[d]
			else:
				found = True
		if proposition is not None and found:
			propositions[e] = proposition
			marks[proposition] += 1

	#print_grove(elves, {})#marks)
	#print()

	new_elves = set()
	for e in elves:
		if e in propositions and marks[propositions[e]] == 1:
			new_elves.add(propositions[e])
		else:
			new_elves.add(e)
	elves = new_elves
	start_dir_index = (start_dir_index + 1) % 4

print_grove(elves, {})

start_x = min(elves, key=lambda e: e.x).x
start_y = min(elves, key=lambda e: e.y).y
end_x = max(elves, key=lambda e: e.x).x + 1
end_y = max(elves, key=lambda e: e.y).y + 1

print((end_x - start_x) * (end_y - start_y) - len(elves))
