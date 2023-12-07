import sys
import functools
from collections import Counter

order = {
	'A': 12,
	'K': 11,
	'Q': 10,
	'J': 9,
	'T': 8,
	'9': 7,
	'8': 6,
	'7': 5,
	'6': 4,
	'5': 3,
	'4': 2,
	'3': 1,
	'2': 0,
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

	s1 = list(reversed(sorted(c1.values())))
	s2 = list(reversed(sorted(c2.values())))
	if s1 != s2:
		return (s1 > s2) - (s2 > s1)
	else:
		m1 = map_hand(h1)
		m2 = map_hand(h2)
		return (m1 > m2) - (m2 > m1)

key=functools.cmp_to_key(compare_hands)
hands_and_bids_sorted = list(sorted(map(parse_line, sys.stdin.read().splitlines()), key=key))
print(sum((i + 1) * b for i, (_, b) in enumerate(hands_and_bids_sorted)))
