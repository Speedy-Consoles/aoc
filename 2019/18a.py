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
def min_moves(board, width, height, my_pos, doors, keys):
	if len(keys) == 0:
		return 0

	cache_key = str(my_pos[0]) + ''.join(sorted(keys.keys())) + str(my_pos[1])
	if cache_key in cache:
		return cache[cache_key]

	distances = dijkstra(board, my_pos)
	reachable_keys = [k for k in keys if keys[k] in distances]
	options = []
	for k in reachable_keys:
		key_pos = keys[k]
		del keys[k]
		board[key_pos[1]][key_pos[0]] = '@'

		door_pos = None
		if k in doors:
			door_pos = doors[k]
			del doors[k]
			board[door_pos[1]][door_pos[0]] = '.'

		board[my_pos[1]][my_pos[0]] = '.'

		options.append(distances[key_pos] + min_moves(board, width, height, key_pos, doors, keys))

		keys[k] = key_pos
		board[key_pos[1]][key_pos[0]] = k

		if door_pos is not None:
			doors[k] = door_pos
			board[door_pos[1]][door_pos[0]] = k.upper()

		board[my_pos[1]][my_pos[0]] = '@'

	result = min(options)
	cache[cache_key] = result
	return result

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
#print(keys)
#print(doors)
#print('\n'.join(''.join(l) for l in board))
print(min_moves(board, width, height, my_pos, doors, keys))
