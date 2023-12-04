import sys
import re
import operator
from collections import defaultdict

PATTERN = re.compile('^(?P<name>[a-z]{4})\\: (?:(?P<number>\\d+)|(?P<operand1>[a-z]{4}) (?P<operator>[-+\\*/]) (?P<operand2>[a-z]{4}))$')
OPERATORS = {
	'+': operator.add,
	'-': operator.sub,
	'*': operator.mul,
	'/': operator.truediv,
}

class Unknown(object):
	def finish(self, monkeys):
		pass

	def eval(self):
		return self

	def __str__(self):
		return 'x'

class Number(object):
	def __init__(self, number):
		self.number = number

	def finish(self, monkeys):
		pass

	def eval(self):
		return Number(self.number)

	def __str__(self):
		return str(self.number)

class Operation(object):
	def __init__(self, operator, operand1_name, operand2_name):
		self.operator = operator
		self.operand1_name = operand1_name
		self.operand2_name = operand2_name

	def finish(self, monkeys):
		self.operand1 = monkeys[self.operand1_name]
		self.operand2 = monkeys[self.operand2_name]
		del self.operand1_name
		del self.operand2_name

	def eval(self):
		operand1 = self.operand1.eval()
		operand2 = self.operand2.eval()
		if type(operand1) != Number or type(operand2) != Number:
			o = Operation(self.operator, None, None)
			del o.operand1_name
			del o.operand2_name
			o.operand1 = operand1
			o.operand2 = operand2
			return o
		return Number(self.operator(operand1.number, operand2.number))

	def __str__(self):
		if self.operator == operator.add:
			operator_string = '+'
		elif self.operator == operator.sub:
			operator_string = '-'
		elif self.operator == operator.mul:
			operator_string = '*'
		else:
			operator_string = '/'

		if type(self.operand1) == Operation:
			operand1_string = '({})'.format(self.operand1)
		else:
			operand1_string = str(self.operand1)

		if type(self.operand2) == Operation:
			operand2_string = '({})'.format(self.operand2)
		else:
			operand2_string = str(self.operand2)

		return '{} {} {}'.format(operand1_string, operator_string, operand2_string)

def sort_expressions(e1, e2):
	if type(e1) == Number:
		assert(type(e2) != Number)
		return e2, e1.number, True
	else:
		assert(type(e2) == Number)
		return e1, e2.number, False

monkeys = {}

for line in sys.stdin.read().splitlines():
	match_dict = PATTERN.match(line).groupdict()
	name = match_dict['name']
	number = match_dict['number']
	if name == 'root':
		equation_names = (match_dict['operand1'], match_dict['operand2'])
	elif name == 'humn':
		monkeys[name] = Unknown()
	elif number is not None:
		monkeys[name] = Number(int(number))
	else:
		monkeys[name] = Operation(
			OPERATORS[match_dict['operator']],
			match_dict['operand1'],
			match_dict['operand2'],
		)

for monkey in monkeys.values():
	monkey.finish(monkeys)

left, right, _ = sort_expressions(monkeys[equation_names[0]].eval(), monkeys[equation_names[1]].eval())

while type(left) != Unknown:
	#print('{} = {}'.format(left, right))
	variable, constant, flip = sort_expressions(left.operand1, left.operand2)
	if left.operator == operator.add:
		right -= constant
	elif left.operator == operator.sub:
		if flip:
			right = constant - right
		else:
			right += constant
	elif left.operator == operator.mul:
		if constant == 0:
			assert(right == 0)
			print('x can be anything for which {} is defined'.format(variable))
			sys.exit()
		right /= constant
	else:
		assert(left.operator == operator.truediv)
		if flip:
			if right == 0:
				assert(constant == 0)
				print('{} != 0'.format(variable))
				sys.exit()
			else:
				right = constant / right
		else:
			assert(constant != 0)
			right *= constant
	left = variable

print('{} = {}'.format(left, right))
