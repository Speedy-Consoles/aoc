import sys

DIRS = {
	'R': ( 1,  0),
	'L': (-1,  0),
	'U': ( 0,  1),
	'D': ( 0, -1),
}

instructions = ((DIRS[line[0]], int(line[2:])) for line in sys.stdin.read().splitlines())
rope = [(0, 0)] * 10
positions = {(0, 0)}
for (xo, yo), n in instructions:
	for i in range(n):
		rope[0] = (rope[0][0] + xo, rope[0][1] + yo)

		for j in range(1, 10):
			dx = rope[j - 1][0] - rope[j][0]
			dy = rope[j - 1][1] - rope[j][1]
			if abs(dx) > 1 or abs(dy) > 1:
				rope[j] = (
					rope[j][0] + max(min(dx, 1), -1),
					rope[j][1] + max(min(dy, 1), -1),
				)
		positions.add(rope[9])

print(len(positions))
