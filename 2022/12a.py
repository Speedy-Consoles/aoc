import sys
from collections import deque

DIRS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def find(needle, grid):
	y = next(i for i, e in enumerate(grid) if needle in e)
	x = next(i for i, e in enumerate(grid[y]) if e == needle)
	return x, y

grid = sys.stdin.read().splitlines()
width = len(grid[0])
height = len(grid)

start = find('S', grid)
end = find('E', grid)

fringe = deque([start])
distance = {start: 0}

while len(fringe) > 0:
	x, y = fringe.popleft()
	h = grid[y][x]
	if h == 'S':
		h = 'a'
	for ox, oy in DIRS:
		nx = x + ox
		ny = y + oy
		if nx in range(width) and ny in range(height):
			if (nx, ny) not in distance:
				nh = grid[ny][nx]
				if nh == 'E':
					nh = 'z'
				if ord(h) >= ord(nh) - 1:
					fringe.append((nx, ny))
					distance[(nx, ny)] = distance[(x, y)] + 1

print(distance[end])
