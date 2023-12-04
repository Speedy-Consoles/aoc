import sys
from collections import deque

def compute_game_string(decks):
	return ','.join(str(x) for x in decks[0]) + '|' + ','.join(str(x) for x in decks[1])

def combat(decks, depth):
	seen_games = set(compute_game_string(decks))

	while len(decks[0]) > 0 and len(decks[1]) > 0:
		game_string = compute_game_string(decks)
		if game_string in seen_games:
			return 0
		seen_games.add(game_string)
		cards = [decks[0].popleft(), decks[1].popleft()]
		if len(decks[0]) >= cards[0] and len(decks[1]) >= cards[1]:
			rec_decks = [
				deque(list(decks[0])[:cards[0]]),
				deque(list(decks[1])[:cards[1]])
			]
			winner = combat(rec_decks, depth + 1)
		else:
			winner = int(cards[0] < cards[1])

		if winner == 0:
			decks[0] += cards
		else:
			decks[1] += cards[::-1]

	return int(cards[0] < cards[1])

deck_strings = sys.stdin.read().split('\n\n')
decks = [deque(int(x) for x in s.splitlines()[1:]) for s in deck_strings]

winner = combat(decks, 0)

s = 0
for i, card in enumerate(reversed(decks[winner])):
	s += (i + 1) * card
print(s)
