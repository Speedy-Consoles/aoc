import sys
import re
from collections import defaultdict

template, rules_string = sys.stdin.read().split('\n\n')
rule_strings = rules_string.splitlines()
rules = {}
for rule_string in rule_strings:
	pair, insertion = rule_string.split(' -> ')
	rules[pair] = insertion

num_pairs = defaultdict(int)
for i in range(len(template) - 1):
	pair = template[i] + template[i + 1]
	num_pairs[pair] += 1

for i in range(40):
	new_num_pairs = defaultdict(int)
	for pair, num in num_pairs.items():
		if pair in rules:
			new_pair1 = pair[0] + rules[pair]
			new_pair2 = rules[pair] + pair[1]
			new_num_pairs[new_pair1] += num
			new_num_pairs[new_pair2] += num
		else:
			new_num_pairs[pair] += num
	num_pairs = new_num_pairs

counter = defaultdict(int)
counter[template[0]] += 1
counter[template[-1]] += 1
for pair, num in num_pairs.items():
	counter[pair[0]] += num
	counter[pair[1]] += num

result = (max(counter.values()) - min(counter.values())) // 2
print(result)
