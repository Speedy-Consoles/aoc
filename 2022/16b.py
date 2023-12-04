import sys
import re
from collections import deque

PATTERN = re.compile('^Valve ([A-Z]{2}) has flow rate=(\\d+); tunnels? leads? to valves? ([A-Z]{2}(?:, [A-Z]{2})*)$')

def find_best(me, me_t, el, el_t, closed, time, flow):
	if time <= 0:
		return 0, []

	if len(closed) == 0:
		if me_t is not None:
			valve = me
			t = me_t
			opener = 'me'
		else:
			valve = el
			t = el_t
			opener = 'el'

		released = flow * time
		if t <= time:
			released += (time - t) * flow_rates[valve]
			steps = [(flow * t, opener, valve, flow + flow_rates[valve])]
		else:
			steps = []
		steps.append((released, None, None, None))
		return released, steps
	else:
		best_released = 0
		best_steps = []
		for i, valve in enumerate(closed):
			if me_t is None:
				new_me = valve
				new_me_t = all_distances[me][valve] + 1
				new_el = el
				new_el_t = el_t
			else:
				new_el = valve
				new_el_t = all_distances[el][valve] + 1
				new_me = me
				new_me_t = me_t

			t = min(new_me_t, new_el_t)

			if time < t:
				released = flow * time
				steps = [(released, None, None, None)]
			else:
				new_closed = closed - {valve}
				new_time = time - t
				base_released = t * flow

				new_me_t -= t
				new_el_t -= t
				if new_me_t == 0:
					new_flow = flow + flow_rates[new_me]
					new_me_t = None
					opener = 'me'
					opened = new_me
				else:
					new_flow = flow + flow_rates[new_el]
					new_el_t = None
					opener = 'el'
					opened = new_el

				#upper_bound = base_release
				#f = new_flow
				#for a, b in zip(*[iter(reversed(sorted(closed - {opened}, key=lambda x: flow_rates[x])))] * 2):
				#	pass
				upper_bound = base_released + new_time * (new_flow + sum(flow_rates[x] for x in closed - {opened}))
				if upper_bound <= best_released:
					continue

				r, s = find_best(
					new_me,
					new_me_t,
					new_el,
					new_el_t,
					new_closed,
					new_time,
					new_flow
				)

				step = (
					base_released,
					opener,
					opened,
					new_flow
				)
				released = base_released + r

				steps = [step] + list(map(lambda x: (x[0] + base_released, x[1], x[2], x[3]), s))

			if released > best_released:
				best_released = released
				best_steps = steps

		return best_released, best_steps

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

best = 0
for i, valve in enumerate(closed):
	print('{}/{}'.format(i, len(closed)))
	released, steps = find_best(valve, all_distances['AA'][valve] + 1, 'AA', None, closed - {valve}, 26, 0)
	if released > best:
		best = released
		best_steps = steps

for step in best_steps:
	print('released: {}, {} opens {}, increasing flow to {}'.format(*step))
print(best)
