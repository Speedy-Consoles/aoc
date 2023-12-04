import sys

def evaluate(term):
	stack = []
	for token in term.replace('(', '( ').replace(')', ' )').split():
		if token.isdigit():
			number = int(token)
		elif token == ')':
			number = stack.pop()
			stack.pop()
		else:
			stack.append(token)
			continue

		if len(stack) == 0:
			stack.append(int(number))
		else:
			last = stack[-1]
			if last == '(':
				stack.append(int(number))
			elif last == '+':
				stack.pop()
				stack[-1] += number
			elif last == '*':
				stack.pop()
				stack[-1] *= number
			else:
				print('ERROR')
				sys.exit(1)

	return stack[0]

print(sum(evaluate(line) for line in sys.stdin.read().splitlines()))
