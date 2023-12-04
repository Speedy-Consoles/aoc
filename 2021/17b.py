from collections import defaultdict
import re

PATTERN = re.compile('target area: x=(-?\\d+)..(-?\\d+), y=(-?\\d+)..(-?\\d+)')

match = PATTERN.match(input())
target_min_x = int(match.group(1))
target_max_x = int(match.group(2))
target_min_y = int(match.group(3))
target_max_y = int(match.group(4))

assert(target_min_x > 0)
assert(target_max_x > 0)
assert(target_min_x <= target_max_x)
assert(target_min_y < 0)
assert(target_max_y < 0)
assert(target_min_y <= target_max_y)

y_velocities = defaultdict(set)
for initial_velocity in range(target_min_y, -target_min_y):
	y = 0
	velocity = initial_velocity
	num_steps = 0
	while y >= target_min_y:
		if y <= target_max_y:
			y_velocities[num_steps].add(initial_velocity)
		y += velocity
		velocity -= 1
		num_steps += 1

max_steps_y = max(y_velocities)

velocities = set()
for initial_x_velocity in range(1, abs(target_max_x) + 1):
	x = 0
	x_velocity = initial_x_velocity
	for num_steps in range(max_steps_y + 1):
		if target_min_x <= x <= target_max_x:
			for initial_y_velocity in y_velocities[num_steps]:
				velocities.add((initial_x_velocity, initial_y_velocity))
		x += x_velocity
		if x_velocity > 0:
			x_velocity -= 1

print(len(velocities))
