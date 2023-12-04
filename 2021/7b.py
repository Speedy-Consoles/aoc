import sys

positions = [int(c) for c in sys.stdin.read().split(',')]

def compute_fuel_use(positions, position):
	fuel_use = 0
	for p in positions:
		distance = abs(p - position)
		fuel_use += distance * (distance + 1) // 2
	return fuel_use

def slow(positions):
	min_position = min(positions)
	max_position = max(positions)

	best_fuel_use = None
	for check_position in range(min_position, max_position + 1):
		fuel_use = compute_fuel_use(positions, check_position)
		if best_fuel_use is None or fuel_use < best_fuel_use:
			best_fuel_use = fuel_use
	return best_fuel_use

#    f  = sum(|p - a| * (|p - a| + 1) / 2)
#       = sum((|p - a| * |p - a| + |p - a|) / 2)
#       = sum(((p - a)^2 + |p - a|) / 2)
#       = sum((p^2 - 2pa + a^2 + |p - a|) / 2)
#   f'  = sum((2p - 2a +- 1) / 2)
#       = sum(p - a +- 1/2)
#       = pn +- n/2 - sum(a)
#    0  = pn +- n/2 - sum(a)
#       = pn +- n/2 - sum(a)
#<=> pn = sum(a) +- n/2
#<=> p  = sum(a) / n +- 1/2

def fast(positions):
	best_position = sum(positions) // len(positions)
	return compute_fuel_use(positions, best_position)

#print(slow(positions))
print(fast(positions))
