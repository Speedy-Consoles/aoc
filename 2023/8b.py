import sys
import re
import math

PATTERN = re.compile('^([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)$')

lines = sys.stdin.read().splitlines()

instructions = [0 if x == 'L' else 1 for x in lines[0]]

graph = {}
for line in lines[2:]:
	src, dst_left, dst_right = PATTERN.match(line).groups()
	graph[src] = (dst_left, dst_right)

def count_steps(node, graph):
	counter = 0
	while not node.endswith('Z'):
		node = graph[node][instructions[counter % len(instructions)]]
		counter += 1
	return counter

print(math.lcm(*(count_steps(start, graph) for start in graph if start.endswith('A'))))

