import math
import re

PATTERN = re.compile('target area: x=(-?\\d+)..(-?\\d+), y=(-?\\d+)..(-?\\d+)')


def compute_velocity(target, num_steps, horizontal):
	velocity_times_num_steps = target + num_steps * (num_steps - 1) // 2

	if horizontal and velocity_times_num_steps < num_steps**2:
		velocity = int(math.sqrt(2 * target + 1 / 4) - 1 / 2)
		if velocity * (velocity + 1) // 2 == target:
			return velocity
		else:
			return None

	if velocity_times_num_steps % num_steps != 0:
		return None

	return velocity_times_num_steps // num_steps


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

possible_velocities = set()
for y in range(target_min_y, target_max_y + 1):
	for x in range(target_min_x, target_max_x + 1):
		for steps in range(1, 200):  # TODO better upper limit
			x_vel = compute_velocity(x, steps, True)
			y_vel = compute_velocity(y, steps, False)
			if x_vel is not None and y_vel is not None:
				possible_velocities.add((x_vel, y_vel))

print(len(possible_velocities))
