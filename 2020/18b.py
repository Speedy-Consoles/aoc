import sys

def evaluate_add(elements):
	stack = []
	for element in elements:
		if type(element) == int and len(stack) > 0 and stack[-1] == '+':
			stack.pop()
			stack[-1] += element
		else:
			stack.append(element)

	return stack

def evaluate_mul(elements):
	stack = []
	for element in elements:
		if type(element) == int and len(stack) > 0 and stack[-1] == '*':
			stack.pop()
			stack[-1] *= element
		else:
			stack.append(element)

	return stack

class Expression(object):
	def __init__(self, tokens):
		self.elements = []
		level = 0
		for token in tokens:
			if level > 0:
				if token == ')':
					level -= 1
					if level == 0:
						self.elements.append(Expression(child_tokens))
				elif token == '(':
					level += 1
				child_tokens.append(token)
			elif token == '(':
				child_tokens = []
				level = 1
			else:
				self.elements.append(token)

	def evaluate(self):
		elements = [e if type(e) != Expression else e.evaluate() for e in self.elements]
		elements = evaluate_add(elements)
		elements = evaluate_mul(elements)
		return elements[0]

	def print(self, indentation=0):
		for e in self.elements:
			if type(e) == Expression:
				e.print(indentation + 1)
			else:
				print('\t' * indentation + str(e))

def evaluate(term):
	string_tokens = term.replace('(', '( ').replace(')', ' )').split()
	expression = Expression([int(st) if st.isdigit() else st for st in string_tokens])
	return expression.evaluate()

print(sum(evaluate(line) for line in sys.stdin.read().splitlines()))
