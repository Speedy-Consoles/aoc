import sys

height_map = [[int(c) for c in line] for line in sys.stdin.read().splitlines()]
width = len(height_map[0])
depth = len(height_map)

risk_level_sum = 0
for y, line in enumerate(height_map):
	for x, height in enumerate(line):
		is_low_point = (
			    (x == 0         or height_map[y][x - 1] > height)
			and (x == width - 1 or height_map[y][x + 1] > height)
			and (y == 0         or height_map[y - 1][x] > height)
			and (y == depth - 1 or height_map[y + 1][x] > height)
		)
		if is_low_point:
			risk_level_sum += height + 1

print(risk_level_sum)
