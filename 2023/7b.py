import sys
import functools
from collections import Counter

order = {
	'A': 12,
	'K': 11,
	'Q': 10,
	'T': 9,
	'9': 8,
	'8': 7,
	'7': 6,
	'6': 5,
	'5': 4,
	'4': 3,
	'3': 2,
	'2': 1,
	'J': 0,
}

def map_hand(hand):
	return [order[h] for h in hand]

def parse_line(s):
	hand, bid_string = s.split()
	return hand, int(bid_string)

def compare_hands(hand_and_bid1, hand_and_bid2):
	h1 = hand_and_bid1[0]
	h2 = hand_and_bid2[0]
	c1 = Counter(h1)
	c2 = Counter(h2)
	j1 = c1['J']
	j2 = c2['J']
	c1['J'] = 0
	c2['J'] = 0

	s1 = list(reversed(sorted(c1.values())))
	s2 = list(reversed(sorted(c2.values())))
	s1[0] += j1
	s2[0] += j2
	if s1 != s2:
		return (s1 > s2) - (s2 > s1)
	else:
		m1 = map_hand(h1)
		m2 = map_hand(h2)
		return (m1 > m2) - (m2 > m1)

key=functools.cmp_to_key(compare_hands)
hands_and_bids_sorted = list(sorted(map(parse_line, sys.stdin.read().splitlines()), key=key))
print(sum((i + 1) * b for i, (_, b) in enumerate(hands_and_bids_sorted)))
