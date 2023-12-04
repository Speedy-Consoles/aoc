import sys

NUM_DAYS = 80

fish = [int(c) for c in sys.stdin.read().split(',')]

for i in range(NUM_DAYS):
	for i in range(len(fish)):
		if fish[i] == 0:
			fish[i] = 6
			fish.append(8)
		else:
			fish[i] -= 1

print(len(fish))
