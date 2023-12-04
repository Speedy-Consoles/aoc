import sys

class Or(object):
	def __init__(self, rule_list):
		self.rule_list = rule_list

	def get_matches(self, string, rules):
		for rule in self.rule_list:
			for match_len in rule.get_matches(string, rules):
				yield match_len

class Concat(object):
	def __init__(self, rule_indices):
		self.rule_indices = rule_indices

	def get_matches(self, string, rules):
		stack = [(0, rules[self.rule_indices[0]].get_matches(string, rules), 0)]
		while len(stack) > 0:
			index, current_gen, start = stack[-1]
			try:
				match_len = next(current_gen)
			except StopIteration:
				stack.pop()
				continue

			if index + 1 < len(self.rule_indices):
				next_gen = rules[self.rule_indices[index + 1]].get_matches(string[start + match_len:], rules)
				stack.append((index + 1, next_gen, start + match_len))
			else:
				yield start + match_len

class Literals(object):
	def __init__(self, literals):
		self.literals = literals

	def get_matches(self, string, rules):
		if string.startswith(self.literals):
			yield len(self.literals)

def build_rule(string):
	if string.startswith('"') and string.endswith('"'):
		return Literals(string[1:-1])
	else:
		or_terms = string.split(' | ')
		if len(or_terms) > 1:
			return Or([Concat([int(number) for number in term.split()]) for term in or_terms])
		else:
			return Concat([int(number) for number in string.split()])


rules_string, messages_string = sys.stdin.read().split('\n\n')


index_rule_strings = [s.split(': ') for s in rules_string.strip().split('\n')]
rules = {}
for index_string, rule_string in index_rule_strings:
	index = int(index_string)

	if index not in (8, 11):
		rules[index] = build_rule(rule_string)

rules[8] = build_rule('42 | 42 8')
rules[11] = build_rule('42 31 | 42 11 31')

num_valid = 0
for message in messages_string.split('\n'):
	for match_len in rules[0].get_matches(message, rules):
		if match_len == len(message):
			num_valid += 1

print(num_valid)

