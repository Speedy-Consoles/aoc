import sys
import operator
import re
from collections import deque

PATTERN = re.compile('''\
Monkey (?P<id>\\d+):
  Starting items: (?P<items_string>\\d+(?:, \\d+)*)
  Operation: new = old (?P<operator>[\\*|\\+]) (?P<operand>old|\\d+)
  Test: divisible by (?P<divisor>\\d+)
    If true: throw to monkey (?P<true_target>\\d+)
    If false: throw to monkey (?P<false_target>\\d+)\
''')

class Monkey(object):
	def __init__(self, s):
		match = PATTERN.match(s)

		self.id = int(match.group('id'))
		self.items = deque(int(x) for x in match.group('items_string').split(', '))

		op = { '+': operator.add, '*': operator.mul }[match.group('operator')]
		if match.group('operand') == 'old':
			self.function = lambda x: op(x, x)
		else:
			self.function = lambda x: op(int(match.group('operand')), x)

		self.divisor = int(match.group('divisor'))
		self.targets = [int(match.group('false_target')), int(match.group('true_target'))]

monkey_strings = sys.stdin.read().strip().split('\n\n')
monkeys = [Monkey(s) for s in monkey_strings]

monkey_businesses = [0] * len(monkeys)
for r in range(20):
	for monkey in monkeys:
		monkey_businesses[monkey.id] += len(monkey.items)
		while len(monkey.items) > 0:
			item = monkey.items.popleft()
			item = monkey.function(item) // 3
			target = monkey.targets[int((item % monkey.divisor) == 0)]
			monkeys[target].items.append(item)

sorted_mbs = sorted(monkey_businesses)
print(sorted_mbs[-1] * sorted_mbs[-2])
