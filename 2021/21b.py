import sys
from collections import defaultdict

STEP_POSSIBILITIES = {
	3: 1,
	4: 3,
	5: 6,
	6: 7,
	7: 6,
	8: 3,
	9: 1,
}

WINNING_SCORE = 21


def num_turn_score_universes(score, position):
	result = defaultdict(lambda: defaultdict(int))
	result[0][score] = 1

	if score >= WINNING_SCORE:
		return result

	for steps, possibilities in STEP_POSSIBILITIES.items():
		new_position = (position - 1 + steps) % 10 + 1
		new_score = score + new_position
		for num_turns, turn_possibilities in num_turn_score_universes(new_score, new_position).items():
			for next_score, score_possibilities in turn_possibilities.items():
				result[num_turns + 1][next_score] += possibilities * score_possibilities

	return result


positions = [int(line.split(': ')[1]) for line in sys.stdin.read().splitlines()]

num_turn_score_universes0 = num_turn_score_universes(0, positions[0])
num_turn_score_universes1 = num_turn_score_universes(0, positions[1])

num_wins0 = 0
num_wins1 = 0
for turn_index0 in range(1, 11):
	num_score_universes0 = num_turn_score_universes0[turn_index0]
	for score0, num_universes0 in num_score_universes0.items():
		first_player_wins = score0 >= WINNING_SCORE
		turn_index1 = turn_index0 - first_player_wins
		num_score_universes1 = num_turn_score_universes1[turn_index1]
		for score1, num_universes1 in num_score_universes1.items():
			second_player_wins = score1 >= WINNING_SCORE
			num_universes = num_universes0 * num_universes1
			num_wins0 += first_player_wins * (not second_player_wins) * num_universes
			num_wins1 += (not first_player_wins) * second_player_wins * num_universes

print(max(num_wins0, num_wins1))
