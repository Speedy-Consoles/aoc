import sys

def compute_depths(node, depth):
	overall_depth = depth
	if node in children:
		for child in children[node]:
			overall_depth += compute_depths(child, depth + 1)
	return overall_depth

children = {}
for line in sys.stdin:
	l = line.rstrip('\n').split(')')
	parent = l[0]
	child = l[1]
	if parent in children:
		children[parent].append(child)
	else:
		children[parent] = [child]

print(compute_depths('COM', 0))

