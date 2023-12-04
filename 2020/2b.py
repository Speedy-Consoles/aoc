import sys
import re

regex = re.compile('^([0-9]+)\\-([0-9]+) ([a-z]): ([a-z]+)$')

valid_count = 0
for s in sys.stdin:
	match = regex.match(s)
	first_pos = int(match.group(1)) - 1
	second_pos = int(match.group(2)) - 1
	letter = match.group(3)
	password = match.group(4)
	first_hit = password[first_pos] == letter
	second_hit = password[second_pos] == letter
	if first_hit != second_hit:
		valid_count += 1
print(valid_count)
