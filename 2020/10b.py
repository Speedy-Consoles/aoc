import sys

joltages = set(int(s.strip()) for s in sys.stdin)

num_paths = {0: 1}
for joltage in joltages:
	num_paths[joltage] = sum(num_paths[other] for other in range(joltage - 3, joltage) if other in num_paths)

print(num_paths[max(joltages)])
