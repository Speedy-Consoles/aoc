import sys
import re
from collections import Counter

template, rules_string = sys.stdin.read().split('\n\n')
rule_strings = rules_string.splitlines()
rules = {}
for rule_string in rule_strings:
	pair, insertion = rule_string.split(' -> ')
	rules[pair] = insertion

for i in range(10):
	insertions = [None] * (len(template) - 1)
	for j in range(len(template) - 1):
		pair = template[j] + template[j + 1]
		if pair in rules:
			insertions[j] = rules[pair]
	new_template = ''
	for j in range(len(template) - 1):
		new_template += template[j]
		if insertions[j] is not None:
			new_template += insertions[j]
	new_template += template[-1]
	template = new_template

counter = Counter(template)
result = max(counter.values()) - min(counter.values())
print(result)
