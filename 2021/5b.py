import math
import sys
import re
from collections import defaultdict

def sign(x):
	return int(math.copysign(1, x)) if x != 0 else 0

line_pattern = re.compile('^(\\d+),(\\d+) -> (\\d+),(\\d+)$')

def points(x0, y0, x1, y1):
	x_diff = x1 - x0
	y_diff = y1 - y0
	x_dir = sign(x_diff)
	y_dir = sign(y_diff)

	x = x0
	y = y0
	while x != x1 or y != y1:
		yield x, y
		x += x_dir
		y += y_dir
	yield x, y

board = defaultdict(int)
for row in sys.stdin.read().splitlines():
	match_object = line_pattern.match(row)
	x0 = int(match_object.group(1))
	y0 = int(match_object.group(2))
	x1 = int(match_object.group(3))
	y1 = int(match_object.group(4))
	for x, y in points(x0, y0, x1, y1):
		board[(x, y)] += 1

print(sum(value > 1 for value in board.values()))
