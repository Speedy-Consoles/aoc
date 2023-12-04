import sys

grid = [[int(x) for x in line] for line in sys.stdin.read().splitlines()]
width = len(grid[0])
height = len(grid)

visible = [[False] * width for y in range(height)]
for y in range(height):
	tallest = -1
	for x in range(width):
		if grid[y][x] > tallest:
			visible[y][x] = True
			tallest = grid[y][x]
	tallest = -1
	for x in reversed(range(width)):
		if grid[y][x] > tallest:
			visible[y][x] = True
			tallest = grid[y][x]

for x in range(height):
	tallest = -1
	for y in range(width):
		if grid[y][x] > tallest:
			visible[y][x] = True
			tallest = grid[y][x]
	tallest = -1
	for y in reversed(range(width)):
		if grid[y][x] > tallest:
			visible[y][x] = True
			tallest = grid[y][x]

print(sum(sum(visible[y]) for y in range(height)))
