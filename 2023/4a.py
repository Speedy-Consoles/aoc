import sys
import re
import math

pattern = re.compile(r'^Card +\d+:((?: +\d+)+) \|((?: +\d+)+)$')

def num_points(s):
	number_lists = map(lambda x: set(map(int, x.split())), pattern.match(s).groups())
	return math.floor(2**(len(set.intersection(*number_lists)) - 1))

print(sum(num_points(line[:-1]) for line in sys.stdin.readlines()))
