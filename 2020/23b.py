class Cup(object):
	def __init__(self, label):
		self.label = label

def make_move(current_cup, cup_map):
	num_cups = len(cup_map)
	first_selected = current_cup.next
	middle_selected = first_selected.next
	last_selected = middle_selected.next
	new_current_cup = last_selected.next

	selected_labels = {first_selected.label, middle_selected.label, last_selected.label}
	destination_label = (current_cup.label - 2) % num_cups + 1
	while destination_label in selected_labels:
		destination_label = (destination_label - 2) % num_cups + 1
	destination_cup = cup_map[destination_label - 1]
	after_destination_cup = destination_cup.next

	destination_cup.next = first_selected
	last_selected.next = after_destination_cup
	current_cup.next = new_current_cup
	return new_current_cup

# create cups
cup_map = [Cup(x + 1) for x in range(1000000)]

# read given cups
given_cups = [cup_map[int(x) - 1] for x in input()]

# connect given cups
for i in range(1, len(given_cups)):
	given_cups[i - 1].next = given_cups[i]

# remaining cups
for i in range(len(given_cups) + 1, 1000000):
	cup_map[i - 1].next = cup_map[i]

#connect given cups with the rest
given_cups[-1].next = cup_map[len(given_cups)]
cup_map[-1].next = given_cups[0]

current_cup = given_cups[0]
for i in range(10000000):
	current_cup = make_move(current_cup, cup_map)

print(cup_map[0].next.label * cup_map[0].next.next.label)
