import sys
from collections import defaultdict

def num_paths(graph, start, visited=set(), twice_used=False):
	if start == 'end':
		return 1
	result = 0
	for neighbor in graph[start]:
		if neighbor == 'start':
			continue
		if neighbor in visited:
			if twice_used:
				continue
			else:
				insert = False
				t = True
		else:
			insert = neighbor[0].islower()
			t = twice_used

		if insert:
			visited.add(neighbor)

		result += num_paths(graph, neighbor, visited, t)

		if insert:
			visited.remove(neighbor)
	return result

graph = defaultdict(set)
for line in sys.stdin.read().splitlines():
	left, right = line.split('-')
	graph[left].add(right)
	graph[right].add(left)

print(num_paths(graph, 'start'))
