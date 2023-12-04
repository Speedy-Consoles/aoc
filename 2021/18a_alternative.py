import sys
from functools import reduce


def explode(number, depth=0):
	new_number = []
	depth = 0
	index = 0
	right = None
	last_number_index = None
	while index < len(number):
		e = number[index]
		if e == '[':
			if depth == 4 and right is None:
				new_number.append(0)

				index += 1
				left = number[index]
				index += 1
				right = number[index]

				if last_number_index is not None:
					new_number[last_number_index] += left

				index += 1
			else:
				depth += 1
				new_number.append(e)
		elif e == ']':
			depth -= 1
			new_number.append(e)
		elif right is not None:
			new_number.append(e + right)
			new_number += number[index + 1:]
			return new_number, True
		else:
			last_number_index = index
			new_number.append(e)
		index += 1

	return new_number, right is not None


def split(number):
	new_number = []
	index = 0
	for i, e in enumerate(number):
		if type(e) == int and e >= 10:
			a = e // 2
			b = e - a
			new_number += ['[', a, b, ']'] + number[i + 1:]
			return new_number, True
		else:
			new_number.append(e)
		index += 1

	return new_number, False


def add(a, b):
	number = ['['] + a + b + [']']
	while True:
		number, changed = explode(number)
		if changed:
			continue
		number, changed = split(number)
		if changed:
			continue
		break
	return number


def magnitude(number):
	stack = []
	for e in number:
		if e == ']':
			stack.append(stack.pop() * 2 + stack.pop() * 3)
		elif type(e) == int:
			stack.append(e)

	return stack[0]


def stackify(nested):
	if type(nested) == list:
		return ['['] + stackify(nested[0]) + stackify(nested[1]) + [']']
	else:
		return [nested]


numbers = [stackify(eval(line)) for line in sys.stdin.read().splitlines()]
result = reduce(add, numbers[1:], numbers[0])
print(magnitude(result))
