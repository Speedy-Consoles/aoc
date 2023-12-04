import sys

horizontal = 0
depth = 0
for line in sys.stdin.read().splitlines():
	split = line.split()
	direction = split[0]
	amount = int(split[1])
	if direction == 'forward':
		horizontal += amount
	elif direction == 'down':
		depth += amount
	elif direction == 'up':
		depth -= amount
	else:
		print('ERROR:', direction)
		sys.exit(1)

print(horizontal * depth)
