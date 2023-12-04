import sys
from collections import defaultdict

RULES = [
	(1, 2, None),
	(4, 4, None),
	(7, 3, None),
	(8, 7, None),
	(3, 5, (1, 2)),
	(9, 6, (3, 5)),
	(0, 6, (1, 2)),
	(6, 6, None),
	(2, 5, (6, 4)),
	(5, 5, None)
]

count = 0
for line in sys.stdin.read().splitlines():
	split = line.split(' | ')
	unique_patterns = [frozenset(x) for x in split[0].split()]
	output_patterns = [frozenset(x) for x in split[1].split()]

	buckets = defaultdict(set)
	for pattern in unique_patterns:
		buckets[len(pattern)].add(pattern)

	mapping = {}
	for digit, n, params in RULES:
		if params is None:
			element = buckets[n].pop()
		else:
			f = lambda x: len(x & mapping[params[0]]) == params[1]
			element = next(filter(f, buckets[n]))
			buckets[n].remove(element)
		mapping[digit] = element

	rmapping = { v: k for k, v in mapping.items() }
	count += sum(10**i * rmapping[pattern] for i, pattern in enumerate(reversed(output_patterns)))

print(count)
