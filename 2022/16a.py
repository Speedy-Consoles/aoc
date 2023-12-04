import sys
import re
from collections import deque

PATTERN = re.compile('^Valve ([A-Z]{2}) has flow rate=(\\d+); tunnels? leads? to valves? ([A-Z]{2}(?:, [A-Z]{2})*)$')

def find_best(current, closed, time, flow):
	best_released = 0
	for valve in closed:
		d = all_distances[current][valve]

		if time - d - 1 < 0:
			released = flow * time
		else:
			new_flow = flow + flow_rates[valve]
			new_time = time - d - 1
			new_closed = closed - set([valve])
			released = (d + 1) * flow + find_best(valve, new_closed, new_time, new_flow)

		if released > best_released:
			best_released = released

	return best_released

graph = {}
flow_rates = {}
for line in sys.stdin.read().splitlines():
	groups = PATTERN.match(line).groups()
	valve = groups[0]
	flow_rate = int(groups[1])
	targets = groups[2].split(', ')
	graph[valve] = targets
	flow_rates[valve] = flow_rate

all_distances = {}
for valve in graph:
	distances = {valve: 0}
	fringe = deque([valve])
	while len(fringe) > 0:
		current = fringe.popleft()
		d = distances[current]
		for other in graph[current]:
			if other not in distances:
				distances[other] = d + 1
				fringe.append(other)
	all_distances[valve] = distances

closed = set(valve for valve, flow_rate in flow_rates.items() if flow_rate > 0)

print(find_best('AA', closed, 30, 0))
