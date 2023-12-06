import math
import sys

def parse_line(s):
	return int(s.split(':')[1].replace(' ', ''))

def get_num_winning_ways(race_time, record_distance):
	half_race_time = race_time / 2
	t1 = math.sqrt(half_race_time**2 - record_distance)
	return len(range(math.ceil(half_race_time - t1), math.floor(half_race_time + t1))) + 1

print(get_num_winning_ways(*map(parse_line, sys.stdin.read().splitlines())))
