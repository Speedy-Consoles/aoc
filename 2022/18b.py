import sys
from collections import deque

DIRS = [
	( 0,  0,  1),
	( 0,  0, -1),
	( 0,  1,  0),
	( 0, -1,  0),
	( 0,  0,  0),
	( 0,  0,  0),
	( 1,  0,  0),
	(-1,  0,  0),
]

grid = set(tuple(map(int, line.split(','))) for line in sys.stdin.read().splitlines())

min_x = min(grid, key=lambda x: x[0])[0] - 1
max_x = max(grid, key=lambda x: x[0])[0] + 1
min_y = min(grid, key=lambda x: x[1])[1] - 1
max_y = max(grid, key=lambda x: x[1])[1] + 1
min_z = min(grid, key=lambda x: x[2])[2] - 1
max_z = max(grid, key=lambda x: x[2])[2] + 1

surface = 0
start_pos = (min_x, min_y, min_z)
fringe = deque([start_pos])
visited = {start_pos}
while len(fringe) > 0:
	p = fringe.popleft()
	for xo, yo, zo in DIRS:
		np = (p[0] + xo, p[1] + yo, p[2] + zo)
		if np[0] >= min_x and np[0] <= max_x and np[1] >= min_y and np[1] <= max_y and np[2] >= min_z and np[2] <= max_z:
			if np in grid:
				surface += 1
			else:
				if np not in visited:
					fringe.append(np)
					visited.add(np)
print(surface)
