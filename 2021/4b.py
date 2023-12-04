import sys

def wins(board, drawn_numbers):
	for row in board:
		if all(number in drawn_numbers for number in row):
			return True
	for j in range(5):
		if all(board[i][j] in drawn_numbers for i in range(5)):
			return True
	return False

def score(board, drawn_numbers, last_drawn_number):
	return last_drawn_number * sum(number for row in board for number in row if number not in drawn_numbers)

input_groups = sys.stdin.read().split('\n\n')
random_numbers = [int(x) for x in input_groups[0].split(',')]
boards = [[[int(c) for c in line.split()] for line in board_string.splitlines()] for board_string in input_groups[1:]]

scores = []
drawn_numbers = set(random_numbers[:4])
for drawn_number in random_numbers[4:]:
	drawn_numbers.add(drawn_number)
	new_boards = []
	for board in boards:
		if wins(board, drawn_numbers):
			scores.append(score(board, drawn_numbers, drawn_number))
		else:
			new_boards.append(board)
	boards = new_boards

print(scores[-1])
