import sys
from collections import defaultdict

def num_paths(graph, start, visited=set()):
	if start == 'end':
		return 1
	result = 0
	for neighbor in graph[start]:
		if neighbor not in visited and neighbor != 'start':
			if neighbor[0].islower():
				visited.add(neighbor)

			result += num_paths(graph, neighbor, visited)

			if neighbor[0].islower():
				visited.remove(neighbor)
	return result

graph = defaultdict(set)
for line in sys.stdin.read().splitlines():
	left, right = line.split('-')
	graph[left].add(right)
	graph[right].add(left)

print(num_paths(graph, 'start'))
