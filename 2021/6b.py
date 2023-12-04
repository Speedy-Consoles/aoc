import sys

NUM_DAYS = 256

num_fish = [0] * 7
for c in sys.stdin.read().split(','):
	num_fish[int(c)] += 1

num_young_fish = [0] * 7

for i in range(NUM_DAYS):
	index = i % 7

	# create new fish
	num_young_fish[(index + 2) % 7] = num_fish[index]

	# collect grown-up fish
	num_fish[index] += num_young_fish[index]
	num_young_fish[index] = 0

print(sum(num_fish) + sum(num_young_fish))
