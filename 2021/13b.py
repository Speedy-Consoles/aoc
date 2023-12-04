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

for fold_string in fold_strings:
	match = fold_pattern.match(fold_string)
	dim_string = match.group(1)
	offset = int(match.group(2))

	new_paper = set()
	for x, y in paper:
		if dim_string == 'x':
			x = offset - abs(x - offset)
		elif dim_string == 'y':
			y = offset - abs(y - offset)
		new_paper.add((x, y))
	paper = new_paper

width = max(paper, key=lambda x: x[0])[0] + 1
height = max(paper, key=lambda x: x[1])[1] + 1

for y in range(height):
	for x in range(width):
		if (x, y) in paper:
			c = '#'
		else:
			c = '.'
		print(c, end='')
	print()
