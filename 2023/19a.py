import sys
import re
import operator

WORKFLOW_PATTERN = re.compile('^([a-z]+){(.*)}$')
RULE_PATTERN = re.compile('^(?:([xmas])(>|<)(\d+):)?([a-z]+|A|R)$')
PART_PATTERN = re.compile('^{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)}$')
OPERATORS = {'>': operator.gt, '<': operator.lt}

def parse_rule(s):
	category, operator_string, threshold_string, result = RULE_PATTERN.match(s).groups()
	if category is None:
		return lambda _: result
	else:
		operator = OPERATORS[operator_string]
		threshold = int(threshold_string)
		return lambda p: result if operator(p[category], threshold) else None

def parse_workflow(s):
	workflow_name, rules_string = WORKFLOW_PATTERN.match(s).groups()
	return workflow_name, list(map(parse_rule, rules_string.split(',')))

def parse_part(s):
	return {c: int(v) for c, v in PART_PATTERN.match(s).groupdict().items()}

def handle_part(part, workflows):
	rules = workflows['in']
	result = None
	while True:
		result = None
		for rule in rules:
			result = rule(part)
			if result in ('A', 'R'):
				return result == 'A'
			elif result is not None:
				rules = workflows[result]
				break

workflow_strings, part_strings = map(str.splitlines, sys.stdin.read().split('\n\n'))

workflows = {name: rules for name, rules in map(parse_workflow, workflow_strings)}
parts = list(map(parse_part, part_strings))

print(sum(sum(part.values()) for part in parts if handle_part(part, workflows)))
