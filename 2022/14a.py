import sys

def print_grid(grid, min_x, min_y, max_x, max_y):
	start_x = min(min_x, 500)
	start_y = min(min_y, 0)
	end_x = max(max_x + 1, 500)
	end_y = max(max_y + 1, 0)

	for y in range(start_y, end_y):
		for x in range(start_x, end_x):
			if x == 500 and y == 0:
				c = '#'
			elif (x, y) in grid:
				c = grid[(x, y)]
			else:
				c = '.'
			print(c, end='')
		print()

paths = [[tuple(map(int, s.split(','))) for s in line.split(' -> ')] for line in sys.stdin.read().splitlines()]
grid = {}
min_y = None
for path in paths:
	current = path[0]
	grid[current] = '#'
	for node in path[1:]:
		dx = node[0] - current[0]
		dy = node[1] - current[1]
		dx = int(dx > 0) - int(dx < 0)
		dy = int(dy > 0) - int(dy < 0)
		while current != node:
			current = (current[0] + dx, current[1] +dy)
			grid[current] = '#'

min_x = min(grid, key=lambda c: c[0])[0]
min_y = min(grid, key=lambda c: c[1])[1]
max_x = max(grid, key=lambda c: c[0])[0]
max_y = max(grid, key=lambda c: c[1])[1]

counter = 0
while True:
	#print_grid(grid, min_x, min_y, max_x, max_y)
	#print()
	p = (500, 0)
	if p in grid:
		print(counter)
		sys.exit()
	falling = True
	while falling:
		falling = False
		for ox in [0, -1, 1]:
			np = (p[0] + ox, p[1] + 1)
			if np[1] > max_y:
				print(counter)
				sys.exit()
			if np not in grid:
				p = np # ;)
				falling = True
				break
	grid[p] = 'o'
	counter += 1

