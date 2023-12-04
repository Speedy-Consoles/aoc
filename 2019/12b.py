import math
from tqdm import tqdm

position_strings = [input()[1:-1].split(',') for i in range(4)]
positions = [[int(s.strip()[2:]) for s in ps] for ps in position_strings]
velocities = [
	[0, 0, 0],
	[0, 0, 0],
	[0, 0, 0],
	[0, 0, 0],
]

loop_time = [None] * 3
initial_dim_pos_vel = list(zip(*positions, *velocities))

print(initial_dim_pos_vel)
for i in tqdm(range(4000000)):
	for j in range(4):
		for d in range(3):
			bigger = sum(1 for x in positions if x[d] > positions[j][d])
			smaller = sum(1 for x in positions if x[d] < positions[j][d])
			velocities[j][d] += bigger - smaller

	for j in range(4):
		for d in range(3):
			positions[j][d] += velocities[j][d]
	dim_pos_vel = list(zip(*positions, *velocities))
	for d in range(3):
		if loop_time[d] is not None:
			continue
		if dim_pos_vel[d] == initial_dim_pos_vel[d]:
			loop_time[d] = i + 1
			print('Loop time for dimension {} is {}'.format(d, i))
			print(positions, velocities)
	if all(x is not None for x in loop_time):
		break

lcm1 = (loop_time[0] * loop_time[1]) // math.gcd(loop_time[0], loop_time[1])
lcm2 = (lcm1 * loop_time[2]) // math.gcd(lcm1, loop_time[2])

print(lcm2)
