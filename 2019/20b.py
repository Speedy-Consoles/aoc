import sys
import collections

DIRS = [(1, 0, 1), (0, 1, 1), (-1, 0, -1), (0, -1, -1)]

def dijkstra(board, pos, target):
	width = max(x[0] for x in board) + 1
	height = max(x[1] for x in board) + 1
	distances = {(pos, 0): 0}
	fringe = collections.deque([(pos, 0)])
	last_distance = 0
	while len(fringe) > 0:
		current = fringe.popleft()
		current_pos, current_level = current
		current_distance = distances[current]
		if current_distance != last_distance:
			print(current_distance, len(fringe))
		last_distance = current_distance
		for d in range(5):
			if d < 4:
				neighbor_pos = (current_pos[0] + DIRS[d][0], current_pos[1] + DIRS[d][1])
				neighbor_level = current_level
			elif current_pos in targets:
				xinner = current_pos[0] > 10 and current_pos[0] < width - 10
				yinner = current_pos[1] > 10 and current_pos[1] < height - 10
				inner = xinner and yinner
				if current_level == 0 and not inner:
					break
				neighbor_pos = targets[current_pos]
				neighbor_level = current_level + (-1 if inner else 1)
			else:
				break
			neighbor = (neighbor_pos, neighbor_level)
			if neighbor in distances:
				continue
			neighbor_distance = current_distance + 1
			if neighbor_pos == target and neighbor_level == 0:
				return neighbor_distance
			elif board[neighbor_pos] == '.':
				fringe.append(neighbor)
				distances[neighbor] = neighbor_distance
	return None

def get_label(board, pos):
	if board[pos] != '.':
		return None
	for xo, yo, d in DIRS:
		label = []
		next_pos = pos
		while True:
			next_pos = (next_pos[0] + xo, next_pos[1] + yo)
			field = board[next_pos]
			if field.isupper() or field.islower():
				label += field
			else:
				break
		if len(label) > 0:
			return ''.join(label[::d])
	return None

board = collections.defaultdict(lambda: ' ')
for y, l in enumerate(sys.stdin):
	for x, c in enumerate(l[:-1]):
		board[(x, y)] = c
width = max(x[0] for x in board) + 1
height = max(x[1] for x in board) + 1

#for y in range(height):
#	print(''.join(board[(x, y)] for x in range(width)))

labels = {}
targets = {}
for y in range(height):
	for x in range(width):
		pos = (x, y)
		label = get_label(board, pos)
		if label is not None:
			if label in labels:
				other = labels[label]
				targets[other] = pos
				targets[pos] = pos
				targets[pos] = other
			else:
				labels[label] = pos

print(dijkstra(board, labels['AA'], labels['ZZ']))
#print(list(labels.keys()))
#print(targets)


