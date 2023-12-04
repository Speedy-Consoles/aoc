import sys
import re

fold_pattern = re.compile('^fold along (x|y)=(\\d+)$')

dots_string, folds_string = sys.stdin.read().split('\n\n')
dot_strings = dots_string.splitlines()
fold_strings = folds_string.splitlines()

paper = set()
for line in dot_strings:
	x, y = [int(x) for x in line.split(',')]
	paper.add((x, y))

match = fold_pattern.match(fold_strings[0])
dim_string = match.group(1)
offset = int(match.group(2))

new_paper = set()
for x, y in paper:
	if dim_string == 'x':
		x = offset - abs(x - offset)
	elif dim_string == 'y':
		y = offset - abs(y - offset)
	new_paper.add((x, y))

print(len(new_paper))
