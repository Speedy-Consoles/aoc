import itertools as it

digits = [int(x) for x in input()]
#digits = [int(x) for x in '12345678']
n = len(digits)
patterns = [None] * n
for i in range(n):
	stretched = sum(([x] * (i + 1) for x in [0, 1, 0, -1]), [])
	patterns[i] = list(it.islice(it.cycle(stretched), 1, n + 1))

for pi in range(100):
	digits = [abs(sum(d * p for d, p in zip(digits, pattern))) % 10 for pattern in patterns]
print(''.join(str(d) for d in digits)[:8])
