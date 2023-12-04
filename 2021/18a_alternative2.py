import sys
from ast import literal_eval
from functools import reduce


class SnailNumber:
	def __init__(self, *args):
		assert(len(args <= 2))
		if len(args) == 1:
			self.make_literal(args[0])
		elif len(args) == 2:
			self.make_pair(args)

	def make_literal(self, literal):
		self.literal = literal
		self.glue = SnailNumber.literal_glue
		self.explode = SnailNumber.literal_explode

	def make_pair(self, pair):
		self.literal = pair
		self.glue = SnailNumber.pair_glue
		self.explode = SnailNumber.pair_explode

	def literal_glue(self, value, side):
		self.literal += value

	def pair_glue(self, value, side):
		glue(self.pair[side], value, side)

	def literal_explode(self, depth):
		return False, [None, None]

	def pair_explode(self, depth=0):
		if depth == 4:
			self.make_literal(0)
			return self.pair
		else:
			changed = False
			for i in range(2):
				sub_changed, fragments = self.pair[i].explode(depth + 1)
				changed = changed or sub_changed
				if fragments[1 - i] is not None:
					self.pair[1 - i].glue(fragments[1 - i], i)
					result = [None, None]
					result[i] = fragments[i]
					return True, result
			return changed, None, None

	def literal_split(self):
		if self.literal >= 10:
			a = self.literal // 2
			b = self.literal - a
			self.make_pair(a, b)
			return True
		return False

	def pair_split(self):
		for number in self.pairs:
			if number.split():
				return True
		return False

	@staticmethod
	def from_list(l):
		left = SnailNumber(l[0]) if type(l[0]) == list else SnailNumber(l[0])
		right = SnailNumber(l[1]) if type(l[1]) == list else SnailNumber(l[1])
		return SnailNumber(left, right)


# TODO
def add(a, b):
	number = [a, b]
	while True:
		number, a, b, changed = explode(number)
		if changed:
			continue
		number, changed = split(number)
		if changed:
			continue
		break
	return number


def magnitude(number):
	if type(number) == list:
		return 3 * magnitude(number[0]) + 2 * magnitude(number[1])
	else:
		return number


numbers = [literal_eval(line) for line in sys.stdin.read().splitlines()]
result = reduce(add, numbers[1:], numbers[0])
print(magnitude(result))
