import sys

platform = sys.stdin.read().splitlines()
width = len(platform[0])
height = len(platform)

load_sum = 0
for x in range(width):
	stop = 0
	for y in range(height):
		item = platform[y][x]
		match item:
			case '#':
				stop = y + 1
			case 'O':
				load_sum += height - stop
				stop += 1

print(load_sum)
