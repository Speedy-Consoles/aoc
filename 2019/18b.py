import sys
import collections

DIRS = ((1, 0), (0, 1), (-1, 0), (0, -1))

def move_coord(c, d):
	return (c[0] + DIRS[d][0], c[1] + DIRS[d][1])

def passable(field):
	return not (field.isupper() or field == '#')

def dijkstra(board, my_pos):
	distances = {my_pos: 0}
	fringe = collections.deque([my_pos])
	while len(fringe) > 0:
		current = fringe.popleft()
		current_distance = distances[current]
		for d in range(4):
			neighbor = move_coord(current, d)
			if neighbor in distances:
				continue
			elif passable(board[neighbor[1]][neighbor[0]]):
				fringe.append(neighbor)
				distances[neighbor] = current_distance + 1
	return distances

cache = {}
def min_moves(board, width, height, positions, doors, keys):
	if len(keys) == 0:
		return 0

	cache_key = (''.join(sorted(keys.keys())), positions[0], positions[1], positions[2], positions[3])
	if cache_key in cache:
		return cache[cache_key]

	options = []
	for r in range(4):
		robot_pos = positions[r]
		distances = dijkstra(board, robot_pos)
		board[robot_pos[1]][robot_pos[0]] = '.'

		for k in list(keys.keys()):
			if keys[k] not in distances:
				continue
			key_pos = keys[k]
			del keys[k]
			board[key_pos[1]][key_pos[0]] = '@'

			positions[r] = key_pos

			door_pos = None
			if k in doors:
				door_pos = doors[k]
				del doors[k]
				board[door_pos[1]][door_pos[0]] = '.'

			options.append(distances[key_pos] + min_moves(board, width, height, positions, doors, keys))

			keys[k] = key_pos
			board[key_pos[1]][key_pos[0]] = k

			if door_pos is not None:
				doors[k] = door_pos
				board[door_pos[1]][door_pos[0]] = k.upper()

		positions[r] = robot_pos
		board[robot_pos[1]][robot_pos[0]] = '@'

	result = min(options)
	cache[cache_key] = result
	return result

board = [[x for x in l] for l in 
'''#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
#####.@.#####
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############'''.split('\n')]
board = [[x for x in l.strip()] for l in sys.stdin]
width = len(board[0])
height = len(board)

doors = {}
keys = {}
for y in range(height):
	for x in range(width):
		pos = (x, y)
		field = board[y][x]
		if field in ('.', '#'):
			continue
		if field == '@':
			my_pos = pos
		elif field.islower():
			keys[field] = pos
		else:
			doors[field.lower()] = pos
positions = [
	(my_pos[0] + 1, my_pos[1] + 1),
	(my_pos[0] - 1, my_pos[1] + 1),
	(my_pos[0] + 1, my_pos[1] - 1),
	(my_pos[0] - 1, my_pos[1] - 1)
]
board[my_pos[1] + 1][my_pos[0] + 1] = '@'
board[my_pos[1] - 1][my_pos[0] + 1] = '@'
board[my_pos[1] + 1][my_pos[0] - 1] = '@'
board[my_pos[1] - 1][my_pos[0] - 1] = '@'
board[my_pos[1]][my_pos[0]] = '#'
board[my_pos[1]][my_pos[0] + 1] = '#'
board[my_pos[1]][my_pos[0] - 1] = '#'
board[my_pos[1] + 1][my_pos[0]] = '#'
board[my_pos[1] - 1][my_pos[0]] = '#'

print(width, height)
print(keys)
print(doors)
print('\n'.join(''.join(l) for l in board))
print(positions)
print(min_moves(board, width, height, positions, doors, keys))
