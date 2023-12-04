import sys

positions = [int(line.split(': ')[1]) for line in sys.stdin.read().splitlines()]

scores = [0, 0]
prev_roll = 100
active_player = 0
num_rolls = 0
while max(scores) < 1000:
	steps = 0
	for i in range(3):
		roll = prev_roll % 100 + 1
		steps += roll
		prev_roll = roll
		num_rolls += 1
	positions[active_player] = (positions[active_player] - 1 + steps) % 10 + 1
	scores[active_player] += positions[active_player]
	active_player = 1 - active_player

print(num_rolls * min(scores))