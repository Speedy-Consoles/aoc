def manhattan(t):
	return abs(t[0]) + abs(t[1])

moves = (input().split(','), input().split(','))
wire_points = ({(0, 0)}, {(0, 0)})

for w in range(2):
	x = 0
	y = 0
	for move in moves[w]:
		d = move[0]
		n = int(move[1:])
		dx = 0
		dy = 0
		if d == 'R':
			dx = 1
		elif d == 'U':
			dy = 1
		elif d == 'L':
			dx = -1
		elif d == 'D':
			dy = -1

		for i in range(n):
			x += dx
			y += dy
			wire_points[w].add((x, y))

intersections = wire_points[0].intersection(wire_points[1])
intersections -= {(0, 0)}
closest_intersection = min(intersections, key=manhattan)
shortest_distance = manhattan(closest_intersection)
print(shortest_distance)
