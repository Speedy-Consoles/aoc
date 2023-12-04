import sys

#def get_id(s):
#	return int(''.join(str(int(c in ('B', 'R'))) for c in s), 2)

#def get_id(s):
#	return sum(int(c in ('B', 'R')) << i for i, c in enumerate(reversed(s)))

#print(max(get_id(l.strip()) for l in sys.stdin))

print(max(sum(int(c in ('B', 'R')) << i for i, c in enumerate(reversed(l.strip()))) for l in sys.stdin))
#print(max(int(''.join(str(int(c in ('B', 'R'))) for c in l.strip()), 2) for l in sys.stdin))
