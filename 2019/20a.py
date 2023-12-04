import sys
import collections

DIRS = [(1, 0, 1), (0, 1, 1), (-1, 0, -1), (0, -1, -1)]

def dijkstra(board, pos):
	distances = {pos: 0}
	fringe = collections.deque([pos])
	while len(fringe) > 0:
		current = fringe.popleft()
		current_distance = distances[current]
		for d in range(5):
			if d < 4:
				neighbor = (current[0] + DIRS[d][0], current[1] + DIRS[d][1])
			elif current in targets:
				neighbor = targets[current]
			else:
				break
			if neighbor in distances:
				continue
			elif board[neighbor] == '.':
				fringe.append(neighbor)
				distances[neighbor] = current_distance + 1
	return distances

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

distances = dijkstra(board, labels['AA'])
print(distances[labels['ZZ']])
#print(list(labels.keys()))
#print(targets)


