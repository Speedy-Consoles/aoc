import sys
import re

PATTERN = re.compile('^Sensor at x=(-?\\d+), y=(-?\\d+): closest beacon is at x=(-?\\d+), y=(-?\\d+)$')

FACTOR = 4000000
#MAX = 20
MAX = 4000000
SIZE = MAX + 1

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

for y in reversed(range(SIZE)):
	if y % 40000 == 0:
		print('{}%'.format(round(y / SIZE * 100)))
	ranges = []
	for sx, sy, bx, by in sensors:
		d = abs(sx - bx) + abs(sy - by)

		#abs(x - sx) + abs(y - sy) <= d
		#abs(x - sx) <= d - abs(y - sy)
		#x - sx <= d - abs(y - sy) && x - sx >= -d + abs(y - sy)
		#x <= d - abs(y - sy) + sx && x >= -d + abs(y - sy) + sx

		t = d - abs(y - sy)
		ranges = add_range(ranges, range(-t + sx, t + sx + 1))
	if ranges[0].start > 0:
		pos = (ranges[0].start - 1, y)
		break
	elif ranges[0].stop < SIZE:
		pos = (ranges[0].stop, y)
		break

print(pos)
print(pos[0] * FACTOR + pos[1])
