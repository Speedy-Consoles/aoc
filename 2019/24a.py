import sys

class Board:
	def __init__(self, input_string):
		lines = input_string.strip().split('\n')
		self.width = len(lines[0])
		self.height = len(lines)
		self.number = 0
		for y, line in enumerate(lines):
			for x, c in enumerate(line):
				if c == '#':
					self.number |= 1 << (y * self.width + x)

	def get_mask(self, x, y):
		return 1 << (y * self.width + x)

	def has_bug(self, x, y):
		return self.number & self.get_mask(x, y)

	def count_bugs(self, x, y):
		count = 0
		for nx, ny in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]:
			if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height:
				continue
			if self.has_bug(nx, ny):
				count += 1
		return count

	def simulate(self):
		new_number = 0
		for y in range(self.height):
			for x in range(self.width):
				has_bug = self.has_bug(x, y)
				bug_count = self.count_bugs(x, y)
				survive = has_bug and bug_count == 1
				spawn = not has_bug and bug_count in (1, 2)
				if survive or spawn:
					new_number |= self.get_mask(x, y)
		self.number = new_number

	def biodiversity(self):
		return self.number

	def draw(self):
		return '\n'.join(
			''.join(
				'#' if self.number & self.get_mask(x, y) else '.' for x in range(self.width)
			) for y in range(self.height)
		)

input_string = '''\
....#
#..#.
#..##
..#..
#....
'''

input_string = sys.stdin.read()

board = Board(input_string)

bds = {board.biodiversity()}
while True:
	board.simulate()
	bd = board.biodiversity()
	if bd in bds:
		print(bd)
		break
	bds.add(bd)
