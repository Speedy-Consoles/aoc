import math
import re
import sys
import operator
from collections import defaultdict
from functools import reduce

line_pattern = re.compile('Game (\d+): (.+)')

def parse_draw(draw_string):
	color_draw_pairs = (color_draw_string.split() for color_draw_string in draw_string.split(', '))
	return defaultdict(int, {pair[1]: int(pair[0]) for pair in color_draw_pairs})

def parse_line(line):
	line = line[:-1]
	draws_string = line_pattern.match(line).groups()[1]
	return map(parse_draw, draws_string.split('; '))

def cube_set_min(set1, set2):
	return {color: max(set1[color], set2[color]) for color in ('red', 'green', 'blue')}

def min_cubes(cube_sets):
	return reduce(cube_set_min, cube_sets)

def power(cube_set):
	return math.prod(cube_set.values())

print(sum(map(power, map(min_cubes, map(parse_line, sys.stdin.readlines())))))
