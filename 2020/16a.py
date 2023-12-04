import sys
import re

rule_regex = re.compile('^[^:]+: ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$')

section_strings = sys.stdin.read().split('\n\n')

rule_strings = section_strings[0].split('\n')
my_ticket = [int(x) for x in section_strings[1].split('\n')[1].split(',')]
nearby_tickets = [[int(x) for x in s.split(',')] for s in section_strings[2].strip().split('\n')[1:]]

ranges = []
for rule_string in rule_strings:
	match = rule_regex.search(rule_string)
	ranges.append((int(match.group(1)), int(match.group(2))))
	ranges.append((int(match.group(3)), int(match.group(4))))

error_rate = 0
for ticket in nearby_tickets:
	for number in ticket:
		if not any(number >= a and number <= b for a, b in ranges):
			error_rate += number

print(error_rate)
