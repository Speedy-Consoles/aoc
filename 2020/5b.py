import sys

def get_id(s):
	return sum(int(c in ('B', 'R')) << i for i, c in enumerate(reversed(s)))

remaining = set(x for x in range(1 << 10))

for l in sys.stdin:
	remaining.remove(get_id(l.strip()))

missing = list(remaining)
for seat in missing:
	remaining.discard(seat - 1)
	remaining.discard(seat + 1)

for seat in remaining:
	print(seat)
