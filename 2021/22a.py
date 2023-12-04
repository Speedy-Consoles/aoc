import sys
import re

PATTERN = re.compile('^(on|off) x=(-?\\d+)\\.\\.(-?\\d+),y=(-?\\d+)\\.\\.(-?\\d+),z=(-?\\d+)\\.\\.(-?\\d+)$')

reactor = set()

for line in sys.stdin.read().splitlines():
	match = PATTERN.match(line)
	on = match.group(1) == 'on'
	x_min = int(match.group(2))
	x_max = int(match.group(3))
	y_min = int(match.group(4))
	y_max = int(match.group(5))
	z_min = int(match.group(6))
	z_max = int(match.group(7))

	if x_min < -50 or x_max > 50 or y_min < -50 or y_max > 50 or z_min < -50 or z_max > 50:
		continue

	for z in range(z_min, z_max + 1):
		for y in range(y_min, y_max + 1):
			for x in range(x_min, x_max + 1):
				if on:
					reactor.add((x, y, z))
				else:
					reactor.discard((x, y, z))

print(len(reactor))
