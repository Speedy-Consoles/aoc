import sys

forest = [s.strip() for s in sys.stdin]
slopes = [
	(1, 1),
	(3, 1),
	(5, 1),
	(7, 1),
	(1, 2),
]
tree_product = 1
for slope_x, slope_y in slopes:
	x = 0
	y = 0
	num_trees = 0
	while y < len(forest):
		num_trees += int(forest[y][x] == '#')
		x += slope_x
		y += slope_y
		x %= len(forest[0])
	tree_product *= num_trees
print(tree_product)
