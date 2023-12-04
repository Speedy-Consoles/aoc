import re

PATTERN = re.compile('target area: x=(-?\\d+)..(-?\\d+), y=(-?\\d+)..(-?\\d+)')

match = PATTERN.match(input())
target_min_y = int(match.group(3))
target_max_y = int(match.group(4))

assert(target_min_y < 0)
assert(target_min_y <= target_max_y)

initial_y_vel = -target_min_y - 1
max_height = initial_y_vel * (initial_y_vel + 1) // 2
print(max_height)
