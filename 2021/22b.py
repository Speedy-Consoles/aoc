import sys
import math
import re


class Cuboid:
	def __init__(self, start, end):
		self.start = start
		self.end = end

	def intersects(self, other):
		for d in range(3):
			s = max(self.start[d], other.start[d])
			e = min(self.end[d], other.end[d])
			if s >= e:
				return False

		return True

	def cut_out(self, other):
		if not self.intersects(other):
			return [Cuboid(self.start[:], self.end[:])]

		remains = []
		rest_start = self.start[:]
		rest_end = self.end[:]
		for d in range(3):
			if rest_start[d] < other.start[d]:
				start = rest_start[:]
				end = rest_end[:]
				end[d] = other.start[d]
				remains.append(Cuboid(start, end))
				rest_start[d] = end[d]
				if rest_start[d] == rest_end[d]:
					break
			if rest_end[d] > other.end[d]:
				start = rest_start[:]
				end = rest_end[:]
				start[d] = other.end[d]
				remains.append(Cuboid(start, end))
				rest_end[d] = start[d]
				if rest_end[d] == rest_start[d]:
					break

		return remains

	def size(self):
		return math.prod(self.end[d] - self.start[d] for d in range(3))


PATTERN = re.compile('^(on|off) x=(-?\\d+)\\.\\.(-?\\d+),y=(-?\\d+)\\.\\.(-?\\d+),z=(-?\\d+)\\.\\.(-?\\d+)$')

cuboids = []
for i, line in enumerate(sys.stdin.read().splitlines()):
	match = PATTERN.match(line)
	on = match.group(1) == 'on'
	x_min = int(match.group(2))
	x_max = int(match.group(3))
	y_min = int(match.group(4))
	y_max = int(match.group(5))
	z_min = int(match.group(6))
	z_max = int(match.group(7))

	start = [x_min, y_min, z_min]
	end = [x_max + 1, y_max + 1, z_max + 1]
	cuboid = Cuboid(start, end)

	new_cuboids = []
	for other_cuboid in cuboids:
		new_cuboids += other_cuboid.cut_out(cuboid)

	if on:
		new_cuboids.append(cuboid)
	cuboids = new_cuboids

num_active_cubes = sum(cuboid.size() for cuboid in cuboids)
print(num_active_cubes)
