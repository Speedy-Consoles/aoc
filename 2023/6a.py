import math
import sys

def parse_line(s):
	return map(int, s.split()[1:])

def get_num_winning_ways(race_time, record_distance):
	return sum(1 for i in range(1, race_time) if (race_time - i) * i > record_distance)

pairs = zip(*map(parse_line, sys.stdin.read().splitlines()))
print(math.prod(get_num_winning_ways(x[0], x[1]) for x in pairs))
