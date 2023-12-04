import sys
from collections import deque

CHAMBER_WIDTH = 7
LEFT_OFFSET = 2
DOWN_OFFSET = 3
ROCK_LIMIT = 1000000000000
DEBUG = False

class Rock(object):
	def __init__(self, *rock_input):
		self.blocks = []
		self.width = 0
		self.height = 0
		for y in reversed(range(len(rock_input))):
			row = rock_input[-y - 1]
			for x, char in enumerate(row):
				if char == '#':
					self.width = max(self.width, x + 1)
					self.height = max(self.height, y + 1)
					self.blocks.append((x, y))

ROCKS = [
	Rock('####'),
	Rock(
		'.#.',
		'###',
		'.#.',
	),
	Rock(
		'..#',
		'..#',
		'###',
	),
	Rock(
		'#',
		'#',
		'#',
		'#',
	),
	Rock(
		'##',
		'##',
	),
]

def print_chamber(chamber, rock, rock_pos):
	for y in reversed(range(rock_pos[1] + rock.height)):
		print('|', end='')
		for x in range(CHAMBER_WIDTH):
			if (x, y) in chamber:
				c = '#'
			elif (x - rock_pos[0], y - rock_pos[1]) in rock.blocks:
				c = '@'
			else:
				c = '.'
			print(c, end='')
		print('|')
	print('+' + '-' * CHAMBER_WIDTH + '+')

def check_collision(chamber, rock, rock_pos):
	if rock_pos[0] < 0 or rock_pos[0] > CHAMBER_WIDTH - rock.width or rock_pos[1] < 0:
		return True
	return any((x + rock_pos[0], y + rock_pos[1]) in chamber for x, y in rock.blocks)

def get_surface(chamber, height):
	start_pos = (0, height)
	fringe = deque([start_pos])
	visited = {start_pos}
	surface = set()
	while len(fringe) > 0:
		p = fringe.popleft()
		for d in [(1, 0), (0, -1), (-1, 0), (0, 1)]:
			np = (p[0] + d[0], p[1] + d[1])
			if np[0] >= 0 and np[0] < CHAMBER_WIDTH and np[1] >= 0 and np[1] <= height and np not in visited:
				if np in chamber:
					surface.add((np[0], np[1] - height))
				else:
					fringe.append(np)
					visited.add(np)
	return surface

jet_input = input()
jet = [-1 if x == '<' else 1 for x in jet_input]

chamber = set()
tower_height = 0
rock_index = 0
jet_index = 0
rock_pos = (LEFT_OFFSET, tower_height + DOWN_OFFSET)
num_rocks = 0
marks = {}
height_hack = None
if DEBUG:
	print_chamber(chamber, ROCKS[rock_index], rock_pos)
while num_rocks < ROCK_LIMIT:
	d = jet[jet_index]

	new_pos = (rock_pos[0] + d, rock_pos[1])
	if not check_collision(chamber, ROCKS[rock_index], new_pos):
		rock_pos = new_pos

	new_pos = (rock_pos[0], rock_pos[1] - 1)
	if not check_collision(chamber, ROCKS[rock_index], new_pos):
		rock_pos = new_pos
	else:
		tower_height = max(tower_height, rock_pos[1] + ROCKS[rock_index].height)
		chamber |= {(x + rock_pos[0], y + rock_pos[1]) for x, y in ROCKS[rock_index].blocks}
		rock_index = (rock_index + 1) % len(ROCKS)
		rock_pos = (LEFT_OFFSET, tower_height + DOWN_OFFSET)
		num_rocks += 1
		surface = frozenset(get_surface(chamber, tower_height))
		key = (rock_index, jet_index, surface)
		if height_hack is None:
			if key in marks:
				other_num_rocks, other_tower_height = marks[key]
				num_rocks_diff = num_rocks - other_num_rocks
				height_diff = tower_height - other_tower_height
				remaining_rocks = ROCK_LIMIT - num_rocks
				num_repetitions = remaining_rocks // num_rocks_diff
				height_hack = num_repetitions * height_diff
				num_rocks += num_repetitions * num_rocks_diff
			else:
				marks[key] = (num_rocks, tower_height)

	if DEBUG:
		print()
		if jet_index > 0:
			print(jet_input[:jet_index], end=' ')
		print(jet_input[jet_index], end='')
		if jet_index < len(jet_input) - 1:
			print(' ' + jet_input[jet_index + 1:], end = '')
		print()
		print_chamber(chamber, ROCKS[rock_index], rock_pos)

	jet_index = (jet_index + 1) % len(jet)

print(num_rocks_diff)
print(height_diff)
print(tower_height + height_hack)
