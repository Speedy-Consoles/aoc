import sys
import re
import math

pattern = re.compile(r'^Card +\d+:((?: +\d+)+) \|((?: +\d+)+)$')

def num_winning_numbers(s):
	number_lists = map(lambda x: set(map(int, x.split())), pattern.match(s).groups())
	return len(set.intersection(*number_lists))

all_num_winning_numbers = list(num_winning_numbers(line[:-1]) for line in sys.stdin.readlines())

num_cards = [1] * len(all_num_winning_numbers)
for i, num_winning_numbers in enumerate(all_num_winning_numbers):
	for j in range(num_winning_numbers):
		num_cards[i + j + 1] += num_cards[i]

print(sum(num_cards))
