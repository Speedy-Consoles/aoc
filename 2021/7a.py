import sys

def median(l):
	ls = sorted(l)
	return ls[len(ls) // 2]

positions = [int(c) for c in sys.stdin.read().split(',')]

align_position = median(positions)
fuel_use = sum(abs(position - align_position) for position in positions)
print(fuel_use)
