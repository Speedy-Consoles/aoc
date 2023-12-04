import sys

dirs = [
	( 1,  0),
	( 0,  1),
	(-1,  0),
	( 0, -1)
]

d = 0
px = 0
py = 0
for l in sys.stdin:
	command = l[0]
	amount = int(l[1:])
	if command == 'N':
		py += amount
	elif command == 'E':
		px += amount
	elif command == 'S':
		py -= amount
	elif command == 'W':
		px -= amount
	elif command == 'R':
		d = (d - amount // 90) % 4
	elif command == 'L':
		d = (d + amount // 90) % 4
	elif command == 'F':
		px += dirs[d][0] * amount
		py += dirs[d][1] * amount

print(abs(px) + abs(py))
