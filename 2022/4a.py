import sys
import re


PATTERN = re.compile('^(\\d+)-(\\d+),(\\d+)-(\\d+)$')

def overlap(r1, r2):
	start = max(r1[0], r2[0])
	end = min(r1[1], r2[1])
	if start >= end:
		return None
	else:
		return (start, end)

def get_ranges(line):
	a, b, x, y = map(int, PATTERN.match(line).groups())
	return (a, b + 1), (x, y + 1)

def has_full_overlap(ranges):
	return overlap(*ranges) in ranges

print(sum(has_full_overlap(get_ranges(line)) for line in sys.stdin.read().splitlines()))
