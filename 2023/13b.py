from itertools import chain
from operator import ne
import sys

DIMENSION_FACTORS = [1, 100]

def curry(f, *fixed_arguments):
	return lambda *x: f(*fixed_arguments, *x)

def get_line(pattern, dimension, index):
	if dimension == 0:
		return (row[index] for row in pattern)
	else:
		return iter(pattern[index])

def get_size(pattern, dimension):
	return len(pattern[0] if dimension == 0 else pattern)

def is_mirror(pattern, dimension, row_index):
	it1 = reversed(range(row_index))
	it2 = range(row_index, get_size(pattern, dimension))
	f = curry(get_line, pattern, dimension)
	element_its = (chain(*map(f, it)) for it in (it1, it2))
	return sum(map(ne, *element_its)) == 1

def get_mirror_line_index(pattern, dimension):
	size = get_size(pattern, dimension)
	f = curry(is_mirror, pattern, dimension)
	return next(filter(f, range(1, size)), None)

def get_mirror_summand(pattern):
	f = curry(get_mirror_line_index, pattern)
	it = enumerate(map(f, range(2)))
	return next(i * DIMENSION_FACTORS[d] for d, i in it if i is not None)

print(sum(map(get_mirror_summand, map(str.split, sys.stdin.read().split('\n\n')))))
