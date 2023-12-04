import sys

rotations = [
	(( 1,  0), ( 0,  1)),
	(( 0, -1), ( 1,  0)),
	((-1,  0), ( 0, -1)),
	(( 0,  1), (-1,  0))
]

def rotate(x, y, deg):
	r = rotations[(deg // 90) % 4]
	return x * r[0][0] + y * r[0][1], x * r[1][0] + y * r[1][1]

wx = 10
wy = 1
px = 0
py = 0
for l in sys.stdin:
	command = l[0]
	amount = int(l[1:])
	if command == 'N':
		wy += amount
	elif command == 'E':
		wx += amount
	elif command == 'S':
		wy -= amount
	elif command == 'W':
		wx -= amount
	elif command == 'R':
		wx, wy = rotate(wx, wy, -amount)
	elif command == 'L':
		wx, wy = rotate(wx, wy, amount)
	elif command == 'F':
		px += wx * amount
		py += wy * amount

print(abs(px) + abs(py))
