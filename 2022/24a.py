import sys
from queue import PriorityQueue
from functools import total_ordering

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

class Valley:
	def __init__(self, width, height, left_blizzards, right_blizzards, up_blizzards, down_blizzards):
		self.width = width
		self.height = height
		self.left_blizzards = left_blizzards
		self.right_blizzards = right_blizzards
		self.up_blizzards = up_blizzards
		self.down_blizzards = down_blizzards

	def from_lines(lines):
		width = len(lines[0])
		height = len(lines)
		left_blizzards = [set() for i in range(width)]
		right_blizzards = [set() for i in range(width)]
		up_blizzards = [set() for i in range(height)]
		down_blizzards = [set() for i in range(height)]
		for y, line in enumerate(lines):
			for x, c in enumerate(line):
				if c == '>':
					right_blizzards[x].add(y)
				elif c == '<':
					left_blizzards[x].add(y)
				elif c == '^':
					up_blizzards[y].add(x)
				elif c == 'v':
					down_blizzards[y].add(x)
		return Valley(width, height, left_blizzards, right_blizzards, up_blizzards, down_blizzards)

	def update(self):
		left_blizzards = self.left_blizzards[1:] + [self.left_blizzards[0]]
		right_blizzards = [self.right_blizzards[-1]] + self.right_blizzards[:-1]
		up_blizzards = self.up_blizzards[1:] + [self.up_blizzards[0]]
		down_blizzards = [self.down_blizzards[-1]] + self.down_blizzards[:-1]
		return Valley(self.width, self.height, left_blizzards, right_blizzards, up_blizzards, down_blizzards)

	def free(self, pos):
		x = pos.x
		y = pos.y
		if x < 0 or x >= self.width or y < 0 or y >= self.height:
			return False
		return y not in self.left_blizzards[x] and y not in self.right_blizzards[x] and x not in self.up_blizzards[y] and x not in self.down_blizzards[y]

	def print(self):
		for y in range(self.height):
			for x in range(self.width):
				c = '.'
				if y in self.left_blizzards[x]:
					if c == '.':
						c = '<'
					else:
						c = 'x'
				if y in self.right_blizzards[x]:
					if c == '.':
						c = '>'
					else:
						c = 'x'
				if x in self.up_blizzards[y]:
					if c == '.':
						c = '^'
					else:
						c = 'x'
				if x in self.down_blizzards[y]:
					if c == '.':
						c = 'v'
					else:
						c = 'x'
				print(c, end='')
			print()

def get_valley(valleys, index):
	while len(valleys) <= index:
		valleys.append(valleys[-1].update())
	return valleys[index]

@total_ordering
class Node(object):
	def __init__(self, position, distance, target):
		self.position = position
		self.distance = distance
		self.prio = distance + position.man_dist(target)

	def __eq__(self, other):
		if not isinstance(other, Node):
			return NotImplemented
		else:
			return other.prio == self.prio

	def __lt__(self, other):
		if not isinstance(other, Node):
			return NotImplemented
		else:
			return self.prio < other.prio

DIRS = [
	Vec(1, 0),
	Vec(0, 1),
	Vec(-1, 0),
	Vec(0, -1),
	Vec(0, 0),
]

lines = [s[1:-1] for s in sys.stdin.read().splitlines()[1:-1]]
valleys = [Valley.from_lines(lines)]

start = Vec(0, -1)
target = Vec(valleys[0].width - 1, valleys[0].height)

fringe = PriorityQueue()
fringe.put(Node(start, 0, target))
visited = {(start, 0)}

while not fringe.empty():
	current = fringe.get()
	for off in DIRS:
		next_pos = current.position + off
		next_dist = current.distance + 1
		if next_pos == target:
			print(next_dist)
			sys.exit()
		elif (next_pos, next_dist) not in visited and (next_pos == start or get_valley(valleys, next_dist).free(next_pos)):
			fringe.put(Node(next_pos, next_dist, target))
			visited.add((next_pos, next_dist))

