import sys
import re
import operator

PATTERN = re.compile('^(?P<name>[a-z]{4})\\: (?:(?P<number>\\d+)|(?P<operand1>[a-z]{4}) (?P<operator>[-+\\*/]) (?P<operand2>[a-z]{4}))$')
OPERATORS = {
	'+': operator.add,
	'-': operator.sub,
	'*': operator.mul,
	'/': operator.truediv,
}

def get_operation(match_dict):
	if match_dict['number'] is not None:
		number = int(match_dict['number'])
		return lambda x: number
	else:
		operator = OPERATORS[match_dict['operator']]
		operand1_name = match_dict['operand1']
		operand2_name = match_dict['operand2']
		return lambda monkeys: operator(monkeys[operand1_name](monkeys), monkeys[operand2_name](monkeys))

monkeys = {}

for line in sys.stdin.read().splitlines():
	match_dict = PATTERN.match(line).groupdict()
	monkeys[match_dict['name']] = get_operation(match_dict)

print(monkeys['root'](monkeys))
