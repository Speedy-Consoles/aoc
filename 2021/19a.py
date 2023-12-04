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
				#print('trying rotation', rotation)
				transformation = Transformation(rotation, p1 - rotation.apply(p2))
				num_matches = sum(1 for p in cloud2 if transformation.apply(p) in cloud1)
				if num_matches >= THRESHOLD:
					return transformation

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

while len(scanners) > 0:
	print('scanners left:', len(scanners))
	new_scanners = []
	for scanner_index, scanner in scanners:
		print('trying to orient scanner', scanner_index)
		transformation = try_orient(beacons, scanner)
		if transformation is not None:
			print('success!')
			for p in scanner:
				beacons.add(transformation.apply(p))
		else:
			new_scanners.append((scanner_index, scanner))
	scanners = new_scanners

print(len(beacons))
