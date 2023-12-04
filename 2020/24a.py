import sys
from collections import defaultdict

tiles = defaultdict(lambda: 0)
for line in sys.stdin.read().splitlines():
	x = 0
	y = 0
	i = 0
	while i < len(line):
		s = line[i]
		if s == 'e':
			x += 1
		elif s == 'w':
			x -= 1
		else:
			s = line[i:i + 2]
			if s == 'ne':
				y += 1
			elif s == 'nw':
				y += 1
				x -= 1
			elif s == 'sw':
				y -= 1
			elif s == 'se':
				x += 1
				y -= 1
			else:
				assert(False)
			i += 1
		i += 1
	tiles[(x, y)] += 1

print(sum(x % 2 for x in tiles.values()))
