import sys

elves = sys.stdin.read().split('\n\n')
sums = (sum(int(lines) for lines in elf.splitlines()) for elf in elves)

top3 = []
for calories in sums:
	if len(top3) < 3:
		top3.append(calories)
	else:
		worst = min(enumerate(top3), key=lambda x: x[1])
		if calories > worst[1]:
			top3[worst[0]] = calories

print(sum(top3))
