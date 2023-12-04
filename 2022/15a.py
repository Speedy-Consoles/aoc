import sys
import re

PATTERN = re.compile('^Sensor at x=(-?\\d+), y=(-?\\d+): closest beacon is at x=(-?\\d+), y=(-?\\d+)$')

#Y = 10
Y = 2000000

def add_range(ranges, new_range):
	if len(new_range) <= 0:
		return ranges[:]

	new_ranges = []
	for r in ranges:
		if r.start > new_range.stop or new_range.start > r.stop:
			# no overlap
			new_ranges.append(r)
		else:
			#overlap
			new_range = range(min(r.start, new_range.start), max(r.stop, new_range.stop))

	new_ranges.append(new_range)

	return new_ranges


sensors = [tuple(map(int, m.groups())) for m in map(PATTERN.match, sys.stdin.read().splitlines())]
beacons = set((bx, by) for sx, sy, bx, by in sensors)

ranges = []
for sx, sy, bx, by in sensors:
	d = abs(sx - bx) + abs(sy - by)

	#abs(x - sx) + abs(Y - sy) <= d
	#abs(x - sx) <= d - abs(Y - sy)
	#x - sx <= d - abs(Y - sy) && x - sx >= -d + abs(Y - sy)
	#x <= d - abs(Y - sy) + sx && x >= -d + abs(Y - sy) + sx

	t = d - abs(Y - sy)
	ranges = add_range(ranges, range(-t + sx, t + sx + 1))

print(ranges)
print(sum(len(r) for r in ranges) - sum(by == Y for bx, by in beacons))
