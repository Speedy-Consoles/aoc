import sys
import re

PATTERN = re.compile('^([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)$')

lines = sys.stdin.read().splitlines()

instructions = [0 if x == 'L' else 1 for x in lines[0]]

graph = {}
for line in lines[2:]:
	src, dst_left, dst_right = PATTERN.match(line).groups()
	graph[src] = (dst_left, dst_right)

current = 'AAA'
counter = 0
while current != 'ZZZ':
	current = graph[current][instructions[counter % len(instructions)]]
	counter += 1

print(counter)

