import re
import sys

DIGIT_MAP = {
	'zero': 0,
	'one': 1,
	'two': 2,
	'three': 3,
	'four': 4,
	'five': 5,
	'six': 6,
	'seven': 7,
	'eight': 8,
	'nine': 9,
}

pattern = re.compile(rf'(?=(\d|{"|".join(DIGIT_MAP)}))')

def parse_digit(s):
	return int(s) if s.isdigit() else DIGIT_MAP[s]

def parse_line(line):
	digits = list(pattern.findall(line[:-1]))
	return parse_digit(digits[0]) * 10 + parse_digit(digits[-1])

print(sum(map(parse_line, sys.stdin.readlines())))
