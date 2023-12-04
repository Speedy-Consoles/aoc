def distance(t):
	return wire_steps[0][t] + wire_steps[1][t]

moves = (input().split(','), input().split(','))
wire_points = ({(0, 0)}, {(0, 0)})
wire_steps = ({}, {})

for w in range(2):
	points = wire_points[w]
	steps = wire_steps[w]
	x = 0
	y = 0
	s = 0
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
			s += 1
			points.add((x, y))
			if (x, y) in steps:
				steps[(x, y)] = min(s, steps[(x, y)])
			else:
				steps[(x, y)] = s

intersections = wire_points[0].intersection(wire_points[1])
intersections -= {(0, 0)}
closest_intersection = min(intersections, key=distance)
shortest_distance = distance(closest_intersection)
print(shortest_distance)
