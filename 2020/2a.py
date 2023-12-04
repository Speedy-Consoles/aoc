import sys
import re

regex = re.compile('^([0-9]+)\\-([0-9]+) ([a-z]): ([a-z]+)$')

valid_count = 0
for s in sys.stdin:
	match = regex.match(s)
	min_count = int(match.group(1))
	max_count = int(match.group(2))
	letter = match.group(3)
	password = match.group(4)
	count = sum(1 for x in password if x == letter)
	if count >= min_count and count <= max_count:
		valid_count += 1
print(valid_count)
