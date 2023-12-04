import sys

offsets = [
	(-1, -1),
	( 0, -1),
	( 1, -1),
	(-1,  0),
	
	( 1,  0),
	(-1,  1),
	( 0,  1),
	( 1,  1)
]

def print_seats(seats):
	for l in seats:
		print(''.join(l))

def step(seats):
	old_seats = [l[:] for l in seats]
	change = False
	width = len(old_seats[0])
	height = len(old_seats)
	for y in range(height):
		for x in range(width):
			if old_seats[y][x] == '.':
				continue
			num_occupied = 0
			for xo, yo in offsets:
				nx = x + xo
				ny = y + yo
				if nx >= 0 and nx < width and ny >= 0 and ny < height:
					if old_seats[ny][nx] == '#':
						num_occupied += 1
			if num_occupied == 0:
				if old_seats[y][x] != '#':
					change = True
				seats[y][x] = '#'
			elif num_occupied >= 4:
				if old_seats[y][x] != 'L':
					change = True
				seats[y][x] = 'L'
	return change

seats = [[x for x in s.strip()] for s in sys.stdin]

#print_seats(seats)
while step(seats):
	#print()
	#print_seats(seats)
	#print(sum(1 for x in ''.join(''.join(l) for l in seats) if x == '#'))
	pass

print(sum(1 for x in ''.join(''.join(l) for l in seats) if x == '#'))
