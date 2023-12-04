import sys

horizontal = 0
depth = 0
aim = 0
for line in sys.stdin.read().splitlines():
	split = line.split()
	direction = split[0]
	amount = int(split[1])
	if direction == 'forward':
		horizontal += amount
		depth += aim * amount
	elif direction == 'down':
		aim += amount
	elif direction == 'up':
		aim -= amount
	else:
		print('ERROR:', direction)
		sys.exit(1)

print(horizontal * depth)
