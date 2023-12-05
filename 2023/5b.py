import sys
import re
import bisect
import itertools

class MapRange:
	def __init__(self, s):
		it = map(int, s.split())
		self.dst_start = next(it)
		self.src_start = next(it)
		self.length = next(it)

class MapRangeSeparator:
	def __init__(self, src_start, dst_start):
		self.src_start = src_start
		self.dst_start = dst_start

	def __repr__(self):
		return f'({self.src_start} -> {self.dst_start})'

MAP_RANGE_KEY = lambda x: x.src_start

# TODO replace with itertools.batched, once it's available
# https://docs.python.org/3/library/itertools.html#itertools.batched
def batched(iterable, n):
	it = iter(iterable)
	while batch := tuple(itertools.islice(it, n)):
		yield batch

def use_map(value_range, almanac_map):
	index = bisect.bisect(almanac_map, value_range.start, key=MAP_RANGE_KEY)

	src_start = value_range.start
	dst_start = value_range.start
	if index > 0:
		dst_start += almanac_map[index - 1].dst_start - almanac_map[index - 1].src_start

	while index < len(almanac_map) and almanac_map[index].src_start < value_range.stop:
		src_stop = almanac_map[index].src_start
		length = src_stop - src_start
		out_range = range(dst_start, dst_start + length)
		if len(out_range) > 0:
			yield out_range
		src_start = src_stop
		dst_start = almanac_map[index].dst_start
		index += 1

	length = value_range.stop - src_start
	out_range = range(dst_start, dst_start + length)
	if len(out_range) > 0:
		yield out_range

def get_seed_range(pair):
	return range(pair[0], pair[0] + pair[1])

def get_map_range_separators(map_range):
	first = MapRangeSeparator(map_range.src_start, map_range.dst_start)
	second_pos = map_range.src_start + map_range.length
	second = MapRangeSeparator(second_pos, second_pos)
	return first, second

def parse_map(s):
	map_ranges = sorted(map(MapRange, s.split('\n')[1:]), key=MAP_RANGE_KEY)
	return [x for map_range in map_ranges for x in get_map_range_separators(map_range)]

def seed_ranges_to_location_ranges(value_ranges, maps):
	for almanac_map in maps:
		value_ranges = [x for value_range in value_ranges for x in use_map(value_range, almanac_map)]
	return value_ranges

sections = sys.stdin.read().rstrip().split('\n\n')
seed_ranges = list(map(get_seed_range, batched(map(int, sections[0][6:].split()), 2)))
maps = list(map(parse_map, sections[1:]))

print(min(seed_ranges_to_location_ranges(seed_ranges, maps), key=lambda x: x.start).start)
