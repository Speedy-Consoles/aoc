import sys

def get_path(node):
	path = []
	while node is not None:
		path.append(node)
		node = parents[node]
	path.reverse()
	return path

parents = {'COM': None}
for line in sys.stdin:
	base, sattelite = line.rstrip('\n').split(')')
	parents[sattelite] = base

my_path = get_path('YOU')
santa_path = get_path('SAN')

for i, (node1, node2) in enumerate(zip(my_path, santa_path)):
	if node1 != node2:
		break

print(len(my_path) + len(santa_path) - 2 * i - 2)
