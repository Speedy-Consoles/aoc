import sys
from collections import Counter

def parse_line(line):
	format1, format2_string = line.split()
	format2 = list(map(int, format2_string.split(',')))
	return format1, format2

def unfold(format1, format2):
	return '?'.join(format1 for _ in range(5)), format2 * 5

def fits(pattern, token):
	return all(p == '?' or p == t for p, t in zip(pattern, token))

def get_num_arrangements(format1, format2, index1=0, index2=0, space_start=0, cache=None):
	if cache is None:
		cache = {}

	num_required = sum(format2[index2:])
	counter = Counter(format1[index1:])
	if num_required > counter['#'] + counter['?']:
		return 0
	elif len(format1) - index1 - num_required > counter['.'] + counter['?']:
		return 0
	elif index2 >= len(format2):
		return 1

	cached = cache.get((index1, index2))
	if cached is not None:
		return cached

	num_arrangements = 0
	max_space = len(format1) - index1 - (num_required + len(format2) - index2 - 1)
	for space in range(space_start, max_space + 1):
		attempt = '.' * space + '#' * format2[index2]
		if fits(format1[index1:], attempt):
			new_index1 = index1 + space + format2[index2]
			num_arrangements += get_num_arrangements(format1, format2, new_index1, index2 + 1, 1, cache)

	cache[(index1, index2)] = num_arrangements

	return num_arrangements

print(sum(get_num_arrangements(*unfold(r1, r2)) for r1, r2 in map(parse_line, sys.stdin.read().splitlines())))

