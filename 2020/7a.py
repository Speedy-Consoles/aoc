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
		number = match.group(1)
		color = match.group(2)
		if number is not None:
			insert_edge(color, container_color)

possible_bags = set()

def collect(node):
	if node in tree:
		children = tree[node]
		for child in children:
			possible_bags.add(child)
			collect(child)

collect('shiny gold')
print(len(possible_bags))
