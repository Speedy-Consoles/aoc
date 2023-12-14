import sys

def get_size(platform, dimension):
	return len(platform[0] if dimension == 0 else platform)

def get_line(platform, dimension, order, index):
	container = platform if dimension == 0 else platform[index]
	if order == 1:
		container = reversed(container)
	if dimension == 0:
		return (row[index] for row in container)
	else:
		return iter(container)

def set_item(platform, first_dimension, first_dimension_order, index1, index2, value):
	x = (index1, index2)[first_dimension]
	y = (index1, index2)[1 - first_dimension]
	if first_dimension_order == 1:
		if first_dimension == 0:
			x = len(platform[0]) - x - 1
		else:
			y = len(platform) - y - 1
	platform[y][x] = value

def roll(platform, dimension, order):
	size1 = get_size(platform, dimension)
	size2 = get_size(platform, 1 - dimension)
	for d2 in range(size2):
		stop = 0
		for d1, item in enumerate(get_line(platform, 1 - dimension, order, d2)):
			match item:
				case '#':
					stop = d1 + 1
				case 'O':
					set_item(platform, dimension, order, d1, d2, '.')
					set_item(platform, dimension, order, stop, d2, 'O')
					stop += 1

def get_round_rock_positions(platform):
	return frozenset((x, y) for y, row in enumerate(platform) for x, item in enumerate(row) if item == 'O')

platform = [list(x) for x in sys.stdin.read().splitlines()]
height = len(platform)

NUM_ITERATIONS = 1000000000

cache = {}
for i in range(NUM_ITERATIONS):
	round_rock_positions = get_round_rock_positions(platform)
	cached_iteration = cache.get(round_rock_positions)
	if cached_iteration is not None:
		cycle_length = i - cached_iteration
		if (NUM_ITERATIONS - i) % cycle_length == 0:
			break
	cache[round_rock_positions] = i

	for j in range(4):
		roll(platform, (j + 1) % 2, j // 2)

print(sum(sum(1 for item in row if item == 'O') * (height - y) for y, row in enumerate(platform)))
