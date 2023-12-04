import sys

def prio(a):
	return ord(a) - ord('a') + 1 if a.islower() else ord(a) - ord('A') + 27

prio_sum = 0
for rucksack in sys.stdin.read().splitlines():
	common = set()
	num_items = len(rucksack) // 2
	first = rucksack[:num_items]
	second = rucksack[num_items:]
	for a in first:
		if a in second:
			common.add(a)
	prio_sum += sum(prio(x) for x in common)

print(prio_sum)

