import sys
from collections import defaultdict

DIRS = [
	( 1,  0),
	( 0,  1),
	(-1,  1),
	(-1,  0),
	( 0, -1),
	( 1, -1)
]

def print_floor(black_tiles):
	black_pixels = { (x * 2 + y, y) for x, y in black_tiles }
	start_x = min(black_pixels, key=lambda sc: sc[0])[0]
	end_x   = max(black_pixels, key=lambda sc: sc[0])[0] + 1
	start_y = min(black_pixels, key=lambda sc: sc[1])[1]
	end_y   = max(black_pixels, key=lambda sc: sc[1])[1] + 1

	start_x = min(start_x, 0)
	end_x   = max(end_x, 1)
	start_y = min(start_y, 0)
	end_y   = max(end_y, 1)
	for y in range(start_y, end_y):
		for x in range(start_x, end_x):
			if (x + y) % 2 == 0:
				if x == 0 and y == 0:
					print('X' if (x, y) in black_pixels else '+', end='')
				else:
					print('#' if (x, y) in black_pixels else 'O', end='')
			else:
				print(' ', end='')
		print()

def read_black_tiles():
	black_tiles = set()
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

		if (x, y) in black_tiles:
			black_tiles.remove((x, y))
		else:
			black_tiles.add((x, y))
	return black_tiles

def flip_tiles(black_tiles):
	num_black_around_white = defaultdict(lambda: 0)
	to_flip = []
	for x, y in black_tiles:
		num_black = 0
		for d in DIRS:
			nx = x + d[0]
			ny = y + d[1]
			if (nx, ny) in black_tiles:
				num_black += 1
			else:
				num_black_around_white[(nx, ny)] += 1
		if num_black == 0 or num_black > 2:
			to_flip.append((x, y))

	for pos in to_flip:
		black_tiles.remove(pos)

	for pos, count in num_black_around_white.items():
		if count == 2:
			black_tiles.add(pos)

black_tiles = read_black_tiles()

#print(len(black_tiles))
#print_floor(black_tiles)

for i in range(100):
	flip_tiles(black_tiles)
	#print(len(black_tiles))
	#print_floor(black_tiles)

print(len(black_tiles))
