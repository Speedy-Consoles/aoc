import sys
import re
import math

pattern = re.compile(r'^Card +\d+:((?: +\d+)+) \|((?: +\d+)+)$')

def num_winning_numbers(s):
	number_lists = map(lambda x: set(map(int, x.split())), pattern.match(s).groups())
	return len(set.intersection(*number_lists))

def num_points(index, all_num_winning_numbers):
	return sum(num_points(index + 1 + i, all_num_winning_numbers) for i in range(all_num_winning_numbers[index])) + 1

all_num_winning_numbers = list(num_winning_numbers(line[:-1]) for line in sys.stdin.readlines())

print(sum(num_points(i, all_num_winning_numbers) for i in range(len(all_num_winning_numbers))))
