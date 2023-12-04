import sys
import re

rule_regex = re.compile('^([a-z]+ [a-z]+) bags contain (.*).$')
child_regex = re.compile('^(\\d) ([a-z]+ [a-z]+)|(:?no other) bags?$')

tree = {}

def insert_edge(parent, child):
	if parent in tree:
		children = tree[parent]
	else:
		children = []
		tree[parent] = children
	children.append(child)

for line in sys.stdin:
	rule_match = rule_regex.search(line.strip())
	container_color = rule_match.group(1)
	content_matches = (child_regex.search(child) for child in rule_match.group(2).split(', '))
	for match in content_matches:
		number_string = match.group(1)
		color = match.group(2)
		if number_string is not None:
			insert_edge(container_color, (int(number_string), color))

def count_bags(node):
	num_bags = 0
	if node in tree:
		children = tree[node]
		for number, child in children:
			num_bags += (count_bags(child) + 1) * number
	return num_bags

print(count_bags('shiny gold'))
