import re
import sys

pattern = re.compile(r"\d")

def parse_line(line):
	digits = list(map(int, pattern.findall(line[:-1])))
	return digits[0] * 10 + digits[-1]

print(sum(map(parse_line, sys.stdin.readlines())))
