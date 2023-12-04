import sys
import collections

class Board:
	def __init__(self, input_string):
		lines = input_string.strip().split('\n')
		self.numbers = collections.defaultdict(lambda: 0)
		for y, line in enumerate(lines):
			for x, c in enumerate(line):
				if c == '#':
					self.numbers[0] |= 1 << (y * 5 + x)

	def get_mask(self, x, y):
		return 1 << (y * 5 + x)

	def has_bug(self, x, y, level):
		return self.numbers[level] & self.get_mask(x, y)

	def count_bugs(self, x, y, level):
		count = 0
		for nx, ny in [(x + 1, y), (x, y + 1), (x - 1, y), (x, y - 1)]:
			if nx < 0 or nx > 4 or ny < 0 or ny > 4:
				continue
			if nx == 2 and ny == 2:
				continue
			if self.has_bug(nx, ny, level):
				count += 1
		if x == 0 and self.has_bug(1, 2, level - 1):
			count += 1
		elif x == 4 and self.has_bug(3, 2, level - 1):
			count += 1
		if y == 0 and self.has_bug(2, 1, level - 1):
			count += 1
		elif y == 4 and self.has_bug(2, 3, level - 1):
			count += 1
		if x == 1 and y == 2:
			count += sum(1 if self.has_bug(0, y, level + 1) else 0 for y in range(5))
		elif x == 3 and y == 2:
			count += sum(1 if self.has_bug(4, y, level + 1) else 0 for y in range(5))
		elif x == 2 and y == 1:
			count += sum(1 if self.has_bug(x, 0, level + 1) else 0 for x in range(5))
		elif x == 2 and y == 3:
			count += sum(1 if self.has_bug(x, 4, level + 1) else 0 for x in range(5))
		return count

	def simulate(self):
		new_numbers = collections.defaultdict(lambda: 0)
		min_level = min(k for k in self.numbers if self.numbers[k] > 0)
		max_level = max(k for k in self.numbers if self.numbers[k] > 0)
		for level in range(min_level - 1, max_level + 2):
			new_number = 0
			for y in range(5):
				for x in range(5):
					if x == 2 and y == 2:
						continue
					has_bug = self.has_bug(x, y, level)
					bug_count = self.count_bugs(x, y, level)
					survive = has_bug and bug_count == 1
					spawn = not has_bug and bug_count in (1, 2)
					if survive or spawn:
						new_number |= self.get_mask(x, y)
			new_numbers[level] = new_number
		self.numbers = new_numbers

	def num_bugs(self):
		count = 0
		for number in self.numbers.values():
			count += bin(number).count('1')
		return count

	def draw(self):
		out = ''
		for level, number in self.numbers.items():
			out += 'Depth ' + str(level) + '\n' + '\n'.join(
				''.join(
					'#' if self.numbers[level] & self.get_mask(x, y) else '.' for x in range(5)
				) for y in range(5)
			) + '\n\n'
		return out

input_string = '''\
....#
#..#.
#.?##
..#..
#....
'''

input_string = sys.stdin.read()

board = Board(input_string)

for i in range(200):
	board.simulate()
print(board.num_bugs())
