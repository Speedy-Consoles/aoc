import sys

def parse_line(line):
	format1, format2_string = line.split()
	format2 = list(map(int, format2_string.split(',')))
	return format1, format2

def fits(pattern, token):
	return all(p == '?' or p == t for p, t in zip(pattern, token))

def get_num_arrangements(format1, format2, space_start=0):
	if len(format2) == 0:
		if '#' in format1:
			return 0
		else:
			return 1

	num_arrangements = 0
	max_space = len(format1) - (sum(format2) + len(format2) - 1)
	for space in range(space_start, max_space + 1):
		attempt = '.' * space + '#' * format2[0]
		if fits(format1, attempt):
			num_arrangements += get_num_arrangements(format1[space + format2[0]:], format2[1:], 1)

	return num_arrangements

print(sum(get_num_arrangements(r1, r2) for r1, r2 in map(parse_line, sys.stdin.read().splitlines())))

