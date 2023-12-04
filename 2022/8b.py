import sys

grid = [[int(x) for x in line] for line in sys.stdin.read().splitlines()]
width = len(grid[0])
height = len(grid)

best = None
for y in range(height):
	for x in range(width):
		tallness = grid[y][x]
		a = 0
		for x2 in range(x + 1, width):
			a += 1
			if grid[y][x2] >= tallness:
				break
		b = 0
		for x2 in reversed(range(0, x)):
			b += 1
			if grid[y][x2] >= tallness:
				break
		c = 0
		for y2 in range(y + 1, height):
			c += 1
			if grid[y2][x] >= tallness:
				break
		d = 0
		for y2 in reversed(range(0, y)):
			d += 1
			if grid[y2][x] >= tallness:
				break
		viewing_distance = a * b * c * d
		if best is None or best < viewing_distance:
			best = viewing_distance

print(best)
