import sys

def bounds(grid):
	x_start = min(grid, key=lambda c: c[0])[0]
	x_end   = max(grid, key=lambda c: c[0])[0] + 1
	y_start = min(grid, key=lambda c: c[1])[1]
	y_end   = max(grid, key=lambda c: c[1])[1] + 1
	z_start = min(grid, key=lambda c: c[2])[2]
	z_end   = max(grid, key=lambda c: c[2])[2] + 1
	return x_start, x_end, y_start, y_end, z_start, z_end

def print_grid(grid):
	x_start, x_end, y_start, y_end, z_start, z_end = bounds(grid)
	for z in range(z_start, z_end):
		print()
		print('z =', z)
		for y in range(y_start, y_end):
			print(''.join('#' if (x, y, z) in grid else '.' for x in range(x_start, x_end)))

grid = {(x, y, 0) for y, line in enumerate(sys.stdin) for x, c in enumerate(line.strip()) if c == '#'}

x_start, x_end, y_start, y_end, z_start, z_end = bounds(grid)

#print_grid(grid)

for i in range(6):
	x_start -= 1
	x_end   += 1
	y_start -= 1
	y_end   += 1
	z_start -= 1
	z_end   += 1

	old_grid = grid.copy()
	for x in range(x_start, x_end):
		for y in range(y_start, y_end):
			for z in range(z_start, z_end):
				current = (x, y, z)
				count = 0
				for xo in range(-1, 2):
					for yo in range(-1, 2):
						for zo in range(-1, 2):
							if xo == 0 and yo == 0 and zo == 0:
								continue
							count += int((x + xo, y + yo, z + zo) in old_grid)
				if current in old_grid:
					if count not in (2, 3):
						grid.remove(current)
				elif count == 3:
					grid.add(current)
	#print('after {} cycles'.format(i + 1))
	#print_grid(grid)

print(len(grid))
