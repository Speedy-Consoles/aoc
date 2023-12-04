position_strings = [input()[1:-1].split(',') for i in range(4)]
positions = [[int(s.strip()[2:]) for s in ps] for ps in position_strings]
velocities = [
	[0, 0, 0],
	[0, 0, 0],
	[0, 0, 0],
	[0, 0, 0],
]

for i in range(1000):
	for j in range(4):
		for d in range(3):
			bigger = sum(1 for x in positions if x[d] > positions[j][d])
			smaller = sum(1 for x in positions if x[d] < positions[j][d])
			velocities[j][d] += bigger - smaller

	for j in range(4):
		for d in range(3):
			positions[j][d] += velocities[j][d]

abs_sum = lambda l: sum(abs(x) for x in l)
print(sum(abs_sum(p) * abs_sum(v) for p, v in zip(positions, velocities)))
