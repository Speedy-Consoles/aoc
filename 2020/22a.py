import sys
from collections import deque

deck_strings = sys.stdin.read().split('\n\n')
decks = [deque(int(x) for x in s.splitlines()[1:]) for s in deck_strings]

while len(decks[0]) > 0 and len(decks[1]) > 0:
	cards = [decks[0].popleft(), decks[1].popleft()]
	if cards[0] > cards[1]:
		decks[0] += cards
	else:
		decks[1] += cards[::-1]

s = 0
for i, card in enumerate(reversed(decks[0] + decks[1])):
	s += (i + 1) * card
print(s)
