import re
import sys

first_pattern = re.compile(r"^\D*(\d).*")
second_pattern = re.compile(r".*(\d)\D*$")

def parse_line(line):
	line = line[:-1]
	a = int(first_pattern.match(line).group(1))
	b = int(second_pattern.match(line).group(1))
	return a * 10 + b

print(sum(map(parse_line, sys.stdin.readlines())))
