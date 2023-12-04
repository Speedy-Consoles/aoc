import sys
from ast import literal_eval

def compare(a, b):
	if type(a) == int and type(b) == int:
		return int(a > b) - int(a < b)
	elif type(a) == list and type(b) == list:
		for x, y in zip(a, b):
			c = compare(x, y)
			if c != 0:
				return c
		return compare(len(a), len(b))
	elif type(a) == int:
		assert(type(b) == list)
		return compare([a], b)
	else:
		assert(type(a) == list and type(b) == int)
		return compare(a, [b])

pairs = [tuple(map(literal_eval, pair_string.split())) for pair_string in sys.stdin.read().split('\n\n')]
print(sum(i + 1 for i, (a, b) in enumerate(pairs) if compare(a, b) == -1))
