import math
import re
import sys
from dataclasses import dataclass

WORKFLOW_PATTERN = re.compile('^([a-z]+){(.*)}$')
RULE_PATTERN = re.compile('^(?:([xmas])(>|<)(\d+):)?([a-z]+|A|R)$')
PART_PATTERN = re.compile('^{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)}$')

def intersect_ranges(range1, range2):
	return range(max(range1.start, range2.start), min(range1.stop, range2.stop))

@dataclass
class Rule:
	category: str
	greater: bool
	threshold: int
	result: str

	def __neg__(self):
		return Rule(self.category, not self.greater, self.threshold + (1 if self.greater else -1), result)

	def get_range(self):
		start = 1
		stop = 4001
		if self.greater:
			start = self.threshold + 1
		else:
			stop = self.threshold
		return range(start, stop)

	def get_inverted_range(self):
		start = 1
		stop = 4001
		if self.greater:
			stop = self.threshold + 1
		else:
			start = self.threshold
		return range(start, stop)

def parse_rule(s):
	category, operator_string, threshold_string, result = RULE_PATTERN.match(s).groups()
	start = 1
	stop = 4001
	if category is None:
		category = 'x'
		threshold = 0
		greater = True
	else:
		threshold = int(threshold_string)
		greater = operator_string == '>'
	return Rule(category, greater, threshold, result)

def parse_workflow(s):
	workflow_name, rules_string = WORKFLOW_PATTERN.match(s).groups()
	return workflow_name, list(map(parse_rule, rules_string.split(',')))

def count_possibilities(workflows, intervals, workflow_name='in'):
	result = 0
	for rule in workflows[workflow_name]:
		category = rule.category
		new_intervals = {c: i for c, i in intervals.items()}
		new_intervals[category] = intersect_ranges(intervals[category], rule.get_range())
		if rule.result == 'A':
			result += math.prod(map(len, new_intervals.values()))
		elif rule.result != 'R':
			result += count_possibilities(workflows, new_intervals, rule.result)
		intervals[category] = intersect_ranges(intervals[category], rule.get_inverted_range())
	return result

workflow_strings = sys.stdin.read().split('\n\n')[0].splitlines()

workflows = {name: rules for name, rules in map(parse_workflow, workflow_strings)}

print(count_possibilities(workflows, {c: range(1, 4001) for c in 'xmas'}))
