import sys
import heapq

from dataclasses import dataclass, field

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

@dataclass(frozen=True)
class Node:
	position: int
	enter_direction_index: int
	num_straight_steps: int

@dataclass(order=True)
class PriorityItem:
	node: Node=field(compare=False)
	priority: int

	def __str__(self):
		return f'pos: {self.node.position}, edi: {self.node.enter_direction_index}, nss: {self.node.num_straight_steps}, p: {self.priority}'

DIRECTIONS = [
	Vec( 1,  0),
	Vec( 0,  1),
	Vec(-1,  0),
	Vec( 0, -1),
]

def in_bounds(position, width, height):
	return position.x >= 0 and position.x < width and position.y >= 0 and position.y < height

def get_distances(city, start, target):
	width = len(city[0])
	height = len(city)

	fringe = []
	distances = {}
	for di, d in enumerate(DIRECTIONS[:2]):
		node = Node(d, di, 1)
		position = start + d
		distance = city[position.y][position.x]
		distances[node] = distance
		priority = distance + position.man_dist(target)
		heapq.heappush(fringe, PriorityItem(node, priority))

	while len(fringe) > 0:
		node = heapq.heappop(fringe).node

		direction_index_offsets = [1, 3]
		if node.num_straight_steps < 3:
			direction_index_offsets.append(0)

		for dio in direction_index_offsets:
			new_direction_index = (node.enter_direction_index + dio) % 4
			direction = DIRECTIONS[new_direction_index]
			new_position = node.position + direction
			if in_bounds(new_position, width, height):
				new_distance = distances.get(node) + city[new_position.y][new_position.x]
				if new_position == target:
					yield new_distance
				else:
					num_straight_steps = 1 if dio != 0 else node.num_straight_steps + 1
					new_node = Node(new_position, new_direction_index, num_straight_steps)
					if new_node not in distances:
						distances[new_node] = new_distance
						priority = new_distance + new_position.man_dist(target)
						heapq.heappush(fringe, PriorityItem(new_node, priority))


city = [list(map(int, line)) for line in sys.stdin.read().splitlines()]

width = len(city[0])
height = len(city)

start = Vec(0, 0)
target = Vec(width - 1, height - 1)

print(min(get_distances(city, start, target)))
