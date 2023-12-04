import sys

def print_energy_levels(energy_levels):
	for row in energy_levels:
		print(''.join(str(e) for e in row))

def flash(energy_levels, x, y):
	width = len(energy_levels[0])
	height = len(energy_levels)
	num_flashes = 1
	for yo in (-1, 0, 1):
		for xo in (-1, 0, 1):
			nx = x + xo
			ny = y + yo
			if nx < 0 or nx >= width or ny < 0 or ny >= height:
				continue
			energy_levels[ny][nx] += 1
			if energy_levels[ny][nx] == 10:
				num_flashes += flash(energy_levels, nx, ny)
	return num_flashes


energy_levels = [[int(c)for c in line] for line in sys.stdin.read().splitlines()]

width = len(energy_levels[0])
height = len(energy_levels)
size = width * height

num_steps = 0
while True:
	num_flashes = 0
	for y, row in enumerate(energy_levels):
		for x in range(width):
			energy_levels[y][x] += 1
			if energy_levels[y][x] == 10:
				num_flashes += flash(energy_levels, x, y)

	for y, row in enumerate(energy_levels):
		for x, energy_level in enumerate(row):
			if energy_level >= 10:
				energy_levels[y][x] = 0

	num_steps += 1

	if num_flashes == size:
		break

print(num_steps)
