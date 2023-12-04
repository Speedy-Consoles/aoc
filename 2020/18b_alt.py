import sys

def evaluate_add(tokens):
	stack = []
	for token in tokens:
		if type(token) == int and len(stack) > 0 and stack[-1] == '+':
			stack.pop()
			stack[-1] += token
		else:
			stack.append(token)

	return stack

def evaluate_mul(tokens):
	stack = []
	for token in tokens:
		if type(token) == int and len(stack) > 0 and stack[-1] == '*':
			stack.pop()
			stack[-1] *= token
		else:
			stack.append(token)

	return stack

def evaluate_tokens(tokens):
	depth = 0
	tokens_no_p = []
	for i, token in enumerate(tokens):
		if token == '(':
			if depth == 0:
				sub_start = i + 1
			depth += 1
		elif token == ')':
			depth -= 1
			if depth == 0:
				tokens_no_p.append(evaluate_tokens(tokens[sub_start:i]))
		elif depth == 0:
			tokens_no_p.append(token)

	tokens_only_mul = evaluate_add(tokens_no_p)
	final_tokens = evaluate_mul(tokens_only_mul)

	if len(final_tokens) != 1:
		print('ERROR')
		sys.exit(1)

	return final_tokens[0]

def evaluate(term):
	string_tokens = term.replace('(', '( ').replace(')', ' )').split()
	return evaluate_tokens([int(st) if st.isdigit() else st for st in string_tokens])

print(sum(evaluate(line) for line in sys.stdin.read().splitlines()))
