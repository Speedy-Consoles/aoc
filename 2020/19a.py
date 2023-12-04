import sys
import re

class Or(object):
	def __init__(self, rule_list):
		self.rule_list = rule_list

	def as_regex(self, rules):
		return '(:?' + '|'.join(rule.as_regex(rules) for rule in self.rule_list) + ')'

class Concat(object):
	def __init__(self, rule_indices):
		self.rule_indices = rule_indices

	def as_regex(self, rules):
		return ''.join(rules[index].as_regex(rules) for index in self.rule_indices)

class Literals(object):
	def __init__(self, literals):
		self.literals = literals

	def as_regex(self, rules):
		return self.literals

def build_rule(string):
	if string.startswith('"') and string.endswith('"'):
		return Literals(string[1:-1])
	else:
		or_terms = string.split(' | ')
		if len(or_terms) > 0:
			return Or([Concat([int(number) for number in term.split()]) for term in or_terms])
		else:
			return Concat([int(number) for number in string.split()])


rules_string, messages_string = sys.stdin.read().split('\n\n')


index_rule_strings = [s.split(': ') for s in rules_string.strip().split('\n')]
rules = {}
for index_string, rule_string in index_rule_strings:
	index = int(index_string)

	rules[index] = build_rule(rule_string)

pattern = re.compile('^' + rules[0].as_regex(rules) + '$')

print(pattern)
print(sum(1 for message in messages_string.split('\n') if pattern.search(message) is not None))

