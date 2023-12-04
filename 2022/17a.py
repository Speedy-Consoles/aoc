import sys

CHAMBER_WIDTH = 7
LEFT_OFFSET = 2
DOWN_OFFSET = 3
ROCK_LIMIT = 2022
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

jet_input = input()
jet = [-1 if x == '<' else 1 for x in jet_input]

chamber = set()
tower_height = 0
rock_index = 0
jet_index = 0
rock_pos = (LEFT_OFFSET, tower_height + DOWN_OFFSET)
num_rocks = 0
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

print(tower_height)
