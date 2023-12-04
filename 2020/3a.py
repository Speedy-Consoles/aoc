import sys

forest = [s.strip() for s in sys.stdin]
slope_x = 3
slope_y = 1
x = 0
y = 0
num_trees = 0
while y < len(forest):
	num_trees += int(forest[y][x] == '#')
	x += slope_x
	y += slope_y
	x %= len(forest[0])
print(num_trees)
