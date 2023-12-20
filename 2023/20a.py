import sys
from enum import Enum
from dataclasses import dataclass, field
from typing import List
from collections import deque, defaultdict

@dataclass
class Module:
	sources: List[str]
	destinations: List[str]

@dataclass
class Broadcaster(Module):
	def receive(self, high, source):
		return high

@dataclass
class FlipFlop(Module):
	on: bool=False

	def receive(self, high, source):
		if high:
			return None
		else:
			self.on = not self.on
			return self.on

@dataclass
class Conjunction(Module):
	def __init__(self, sources, destinations):
		self.most_recent_high = {source: False for source in sources}
		super().__init__(sources, destinations)

	def receive(self, high, source):
		self.most_recent_high[source] = high
		return not all(self.most_recent_high.values())

@dataclass
class Pulse:
	source: str
	destination: str
	high: bool

def parse_module(s):
	type_and_name, destinations_string = s.split(' -> ')
	destinations = destinations_string.split(', ')
	if type_and_name == 'broadcaster':
		module_type = Broadcaster
		name = type_and_name
	else:
		name = type_and_name[1:]
		if type_and_name[0] == '%':
			module_type = FlipFlop
		else:
			module_type = Conjunction

	return name, module_type, destinations

module_tuples = list(map(parse_module, sys.stdin.read().splitlines()))
sources = defaultdict(list)
for source, _, destinations in module_tuples:
	for destination in destinations:
		sources[destination].append(source)
modules = {name: module_type(sources[name], destinations) for name, module_type, destinations in module_tuples}

num_pulses = {False: 0, True: 0}

for i in range(1000):
	pulses = deque([Pulse('button module', 'broadcaster', False)])
	while len(pulses) > 0:
		pulse = pulses.popleft()
		num_pulses[pulse.high] += 1
		module = modules.get(pulse.destination)
		if module is not None:
			reaction = module.receive(pulse.high, pulse.source)
			if reaction is not None:
				pulses += (Pulse(pulse.destination, destination, reaction) for destination in module.destinations)
print(num_pulses[False] * num_pulses[True])
