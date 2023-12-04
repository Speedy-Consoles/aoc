import re
import sys
from collections import defaultdict

line_pattern = re.compile('Game (\d+): (.+)')

def parse_draw(draw_string):
	color_draw_pairs = (color_draw_string.split() for color_draw_string in draw_string.split(', '))
	return defaultdict(int, {pair[1]: int(pair[0]) for pair in color_draw_pairs})

def parse_line(line):
	line = line[:-1]
	game_id_string, draws_string = line_pattern.match(line).groups()
	game_id = int(game_id_string)
	draws = map(parse_draw, draws_string.split('; '))

	return game_id, draws

def is_possible(draws):
	return all(map(lambda x: x['red'] <= 12 and x['green'] <= 13 and x['blue'] <= 14, draws))

print(sum(map(lambda x: x[0], filter(lambda x: is_possible(x[1]), map(parse_line, sys.stdin.readlines())))))
