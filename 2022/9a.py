import sys

DIRS = {
	'R': ( 1,  0),
	'L': (-1,  0),
	'U': ( 0,  1),
	'D': ( 0, -1),
}

instructions = ((DIRS[line[0]], int(line[2:])) for line in sys.stdin.read().splitlines())

head = (0, 0)
tail = (0, 0)
positions = {(0, 0)}
for (dx, dy), n in instructions:
	for i in range(n):
		old_head = head
		head = (head[0] + dx, head[1] + dy)

		if abs(head[0] - tail[0]) > 1 or abs(head[1] - tail[1]) > 1:
			tail = old_head
			positions.add(tail)

print(len(positions))
