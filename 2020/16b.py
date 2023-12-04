import sys
import re
import math

def fits(number, ranges):
	fits1 = number >= ranges[0][0] and number <= ranges[0][1]
	fits2 = number >= ranges[1][0] and number <= ranges[1][1]
	return fits1 or fits2

rule_regex = re.compile('^([^:]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)$')

section_strings = sys.stdin.read().split('\n\n')

rule_strings = section_strings[0].split('\n')
my_ticket = [int(x) for x in section_strings[1].split('\n')[1].split(',')]
nearby_tickets = [[int(x) for x in s.split(',')] for s in section_strings[2].strip().split('\n')[1:]]

num_fields = len(my_ticket)

rules = {}
for rule_string in rule_strings:
	match = rule_regex.search(rule_string)
	rules[match.group(1)] = (
		(int(match.group(2)), int(match.group(3))),
		(int(match.group(4)), int(match.group(5)))
	)

valid_tickets = []

for ticket in nearby_tickets + [my_ticket[:]]:
	all_fittable = True
	for number in ticket:
		if not any(fits(number, ranges) for ranges in rules.values()):
			all_fittable = False
			break
	if all_fittable:
		valid_tickets.append(ticket)

possibilities = {i: set() for i in range(num_fields)}
for i in range(num_fields):
	for field, ranges in rules.items():
		if all(fits(ticket[i], ranges) for ticket in valid_tickets):
			possibilities[i].add(field)

field_indices = {}

changed = True
while changed:
	changed = False
	for index, fields in possibilities.items():
		if len(fields) == 1:
			field = fields.pop()
			field_indices[field] = index
			del possibilities[index]
			for i, r in possibilities.items():
				r.discard(field)
			changed = True
			break

print(math.prod(my_ticket[index] for field, index in field_indices.items() if field.startswith('departure')))
		
