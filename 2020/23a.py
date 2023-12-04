def rotate(l, i):
	return l[i:] + l[:i]

def move(cups):
	num_cups = len(cups)
	selected_cups = cups[1:4]
	cups = [cups[0]] + cups[4:]
	destination_cup = (cups[0] - 1 - 1) % num_cups + 1
	while destination_cup in selected_cups:
		destination_cup = (destination_cup - 1 - 1) % num_cups + 1
	destination_index = cups.index(destination_cup)
	return cups[1:destination_index + 1] + selected_cups + cups[destination_index + 1:] + [cups[0]]

cups = [int(x) for x in input()]

for i in range(100):
	cups = move(cups)

one_index = cups.index(1)
print(''.join(str(x) for x in rotate(cups, one_index)[1:]))
