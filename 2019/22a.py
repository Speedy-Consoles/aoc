import sys

def cut(cards, index):
	return cards[index:] + cards[:index]

def deal_in_increments(cards, n):
	lc = len(cards)
	result = [0] * lc
	index = 0
	for i in range(lc):
		result[index] = cards[i]
		index += n
		index %= lc
	return result

cards = list(range(10007))

for l in sys.stdin:
	if l[0] == 'c':
		cards = cut(cards, int(l.split()[-1]))
	elif l[5] == 'i':
		cards = cards[::-1]
	else:
		cards = deal_in_increments(cards, int(l.split()[-1]))

print(cards.index(2019))
