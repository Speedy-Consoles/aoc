import sys

DIRS = [
	( 0,  0,  1),
	( 0,  0, -1),
	( 0,  1,  0),
	( 0, -1,  0),
	( 1,  0,  0),
	(-1,  0,  0),
]

grid = set(tuple(map(int, line.split(','))) for line in sys.stdin.read().splitlines())

surface = 0
for x, y, z in grid:
	for xo, yo, zo in DIRS:
		np = (x + xo, y + yo, z + zo)
		if np not in grid:
			surface += 1
print(surface)
