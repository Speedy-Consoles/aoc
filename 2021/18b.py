import sys
from ast import literal_eval


def copy(number):
	if type(number) == list:
		return [copy(number[0]), copy(number[1])]
	else:
		return number


def glue(number, index, value):
	if type(number) == list:
		glued = glue(number[index], index, value)
		number[index] = glued
		return number
	else:
		return number + value


def explode(number, depth=0):
	if type(number) == list:
		if depth == 4:
			return 0, number[0], number[1], True
		else:
			new_number0, a, b, changed = explode(number[0], depth + 1)
			if b is not None:
				number[1] = glue(number[1], 0, b)
			if changed:
				return [new_number0, number[1]], a, None, True

			new_number1, a, b, changed = explode(number[1], depth + 1)
			if a is not None:
				number[0] = glue(number[0], 1, a)
			if changed:
				return [number[0], new_number1], None, b, True

	return number, None, None, False


def split(number):
	if type(number) == list:
		new_number0, changed = split(number[0])
		if changed:
			return [new_number0, number[1]], True
		new_number1, changed = split(number[1])
		if changed:
			return [number[0], new_number1], True
	elif number >= 10:
		a = number // 2
		b = number - a
		return [a, b], True

	return number, False


def add(a, b):
	number = [copy(a), copy(b)]
	while True:
		number, a, b, changed = explode(number)
		if changed:
			continue
		number, changed = split(number)
		if changed:
			continue
		break
	return number


def magnitude(number):
	if type(number) == list:
		return 3 * magnitude(number[0]) + 2 * magnitude(number[1])
	else:
		return number


numbers = [literal_eval(line) for line in sys.stdin.read().splitlines()]
max_magnitude = 0
for i, a in enumerate(numbers):
	for b in numbers[i + 1:]:
		max_magnitude = max(max_magnitude, magnitude(add(a, b)), magnitude(add(b, a)))
print(max_magnitude)
