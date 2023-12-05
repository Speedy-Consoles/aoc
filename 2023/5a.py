import sys
import re
import bisect

class MapRange:
	def __init__(self, s):
		it = map(int, s.split())
		self.dst_start = next(it)
		self.src_start = next(it)
		self.length = next(it)

RANGE_KEY = lambda x: x.src_start

def use_map(value, almanac_map):
	index = bisect.bisect(almanac_map, value, key=RANGE_KEY)
	if index > 0 and index <= len(almanac_map):
		map_range = almanac_map[index - 1]
		offset = value - map_range.src_start
		if offset < map_range.length:
			return map_range.dst_start + offset

	return value

def parse_map(s):
	return sorted(map(MapRange, s.split('\n')[1:]), key=RANGE_KEY)

def seed_to_location(value, maps):
	for almanac_map in maps:
		value = use_map(value, almanac_map)
	return value

sections = sys.stdin.read().rstrip().split('\n\n')
seeds = list(map(int, sections[0][6:].split()))
maps = list(map(parse_map, sections[1:]))

print(min(seed_to_location(seed, maps) for seed in seeds))
