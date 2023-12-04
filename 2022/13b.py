import sys
from ast import literal_eval
from functools import cmp_to_key

def compare(a, b):
	if type(a) == int and type(b) == int:
		return int(a > b) - int(a < b)
	elif type(a) == list and type(b) == list:
		for x, y in zip(a, b):
			c = compare(x, y)
			if c != 0:
				return c
		return compare(len(a), len(b))
	elif type(a) == int:
		assert(type(b) == list)
		return compare([a], b)
	else:
		assert(type(a) == list and type(b) == int)
		return compare(a, [b])

DIVIDER_PACKETS = [[[2]], [[6]]]
packets = [x for pair_string in sys.stdin.read().split('\n\n') for x in map(literal_eval, pair_string.split())] + DIVIDER_PACKETS
sorted_packets = sorted(packets, key=cmp_to_key(compare))
iterator = (i + 1 for i, packet in enumerate(sorted_packets) if packet in DIVIDER_PACKETS)
print(next(iterator) * next(iterator))
