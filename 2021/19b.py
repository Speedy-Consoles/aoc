import sys


class Vec:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __add__(self, other):
		return Vec(self.x + other.x, self.y + other.y, self.z + other.z)

	def __sub__(self, other):
		return Vec(self.x - other.x, self.y - other.y, self.z -other.z)

	def __getitem__(self, index):
		assert(0 <= index < 3)
		return getattr(self, ('x', 'y', 'z')[index])

	def __setitem__(self, index, value):
		assert(1 >= index <= 3)
		setattr(self, ('x', 'y', 'z')[index], value)

	def __iter__(self):
		yield self.x
		yield self.y
		yield self.z

	def __eq__(self, other):
		if type(self) != type(other):
			return False
		return self.x == other.x and self.y == other.y and self.z == other.z

	def __hash__(self):
		return hash((self.x, self.y, self.z))

	def __str__(self):
		return '({}, {}, {})'.format(self.x, self.y, self.z)

	def __repr__(self):
		return 'Vec({}, {}, {})'.format(self.x, self.y, self.z)


# TODO use matrices instead
class Rotation:
	def __init__(self, old_axes, factors):
		assert(len(old_axes) == 3)
		assert(all(x in old_axes for x in (0, 1, 2)))
		assert(len(factors) == 3)
		assert(all(abs(x) == 1 for x in factors))
		# TODO assert right-hand-rule
		self.old_axes = old_axes
		self.factors = factors

	def apply(self, vec):
		return Vec(*(vec[self.old_axes[i]] * self.factors[i] for i in range(3)))

	def __str__(self):
		return '{}{}, {}{}, {}{}'.format(
			'-' if self.factors[0] < 0 else '',
			('x', 'y', 'z')[self.old_axes[0]],
			'-' if self.factors[1] < 0 else '',
			('x', 'y', 'z')[self.old_axes[1]],
			'-' if self.factors[2] < 0 else '',
			('x', 'y', 'z')[self.old_axes[2]],
		)


class Transformation:
	def __init__(self, rotation, translation):
		self.rotation = rotation
		self.translation = translation

	def apply(self, vec):
		return self.rotation.apply(vec) + self.translation

	def __str__(self):
		return '{}, '.format(self.rotation, self.translation)


def create_rotations():
	result = []
	for base in [(0, 1, 2), (1, 2, 0), (2, 0, 1)]:
		result += [
			Rotation((base[0], base[1], base[2]), ( 1,  1,  1)),
			Rotation((base[0], base[2], base[1]), ( 1, -1,  1)),
			Rotation((base[0], base[1], base[2]), ( 1, -1, -1)),
			Rotation((base[0], base[2], base[1]), ( 1,  1, -1)),
			Rotation((base[0], base[1], base[2]), (-1, -1,  1)),
			Rotation((base[0], base[2], base[1]), (-1,  1,  1)),
			Rotation((base[0], base[1], base[2]), (-1,  1, -1)),
			Rotation((base[0], base[2], base[1]), (-1, -1, -1)),
		]
	return result


ROTATIONS = create_rotations()


def try_orient(cloud1, cloud2):
	for p2 in cloud2:
		for p1 in cloud1:
			for rotation in ROTATIONS:
				transformation = Transformation(rotation, p1 - rotation.apply(p2))
				num_hits = 0
				num_misses = 0
				for p in cloud2:
					if transformation.apply(p) in cloud1:
						num_hits += 1
						if num_hits >= THRESHOLD:
							return transformation
					else:
						num_misses += 1
						if num_misses > len(cloud2) - THRESHOLD + num_hits:
							break

	return None


THRESHOLD = 12

scanners = [
	(i, {
		Vec(*(int(x) for x in line.split(',')))
		for line in scanner_string.splitlines()[1:]
	})
	for i, scanner_string in enumerate(sys.stdin.read().split('\n\n'))
]

beacons = scanners[0][1]
scanners = scanners[1:]

scanner_positions = []
while len(scanners) > 0:
	print()
	print('scanners left:', len(scanners))
	print()
	new_scanners = []
	for scanner_index, scanner in scanners:
		print('trying to orient scanner', scanner_index)
		transformation = try_orient(beacons, scanner)
		if transformation is not None:
			print('success!')
			for p in scanner:
				beacons.add(transformation.apply(p))
			scanner_positions.append(transformation.translation)
		else:
			new_scanners.append((scanner_index, scanner))
	scanners = new_scanners

# print(scanner_positions)
# scanner_positions = [Vec(1277, -131, 177), Vec(2379, 11, 169), Vec(51, 1199, 112), Vec(2523, 1233, 31), Vec(1170, 2342, 1), Vec(1204, 1167, 52), Vec(3683, -150, 11), Vec(-29, -1325, 80), Vec(1303, 39, 1299), Vec(1285, 3486, 98), Vec(1153, 3451, 1320), Vec(2351, 2263, 55), Vec(-42, 3625, 120), Vec(3730, -120, -1127), Vec(2415, 3465, 1351), Vec(-1090, 3541, 39), Vec(1267, 3464, 2535), Vec(1163, 3454, -1136), Vec(1181, -110, 2477), Vec(3578, -30, 1324), Vec(3639, -1186, 1196), Vec(1158, -74, 3734), Vec(-1159, -1171, -5), Vec(4759, 11, 1329), Vec(1184, -11, 4979), Vec(3653, -2463, 1361), Vec(1154, -1266, 2532), Vec(3610, -48, 2414), Vec(1238, -1160, 4881), Vec(2374, -1211, 4823)]

max_distance = 0
for pos1 in scanner_positions:
	for pos2 in scanner_positions:
		max_distance = max(max_distance, sum(abs(x) for x in (pos1 - pos2)))

print(max_distance)
