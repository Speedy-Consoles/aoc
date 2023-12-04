import re
import sys

digits = {
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

digit_base = rf'\d|{"|".join(digits)}'
digit = rf'({digit_base})'
not_a_digit = rf'(?:(?!{digit_base}).)'

first_pattern = re.compile(rf'^{not_a_digit}*{digit}.*$')
second_pattern = re.compile(rf'^.*{digit}{not_a_digit}*$')

def parse_digit(s):
	return int(s) if s.isdigit() else digits[s]

def parse_line(line):
	line = line[:-1]
	a = parse_digit(first_pattern.match(line).group(1))
	b = parse_digit(second_pattern.match(line).group(1))
	return a * 10 + b

print(sum(map(parse_line, sys.stdin.readlines())))
