import sys

def count_size(node):
	global s
	if type(node) == int:
		return node

	size = sum(map(count_size, node.values()))
	if size <= 100000:
		s += size
	return size

lines = sys.stdin.read().splitlines()

filesystem = {}
current = filesystem
path = []

index = 0
while index < len(lines):
	line = lines[index]
	if line == "$ cd /":
		current = filesystem
		path = []
	elif line == "$ cd ..":
		current = path.pop()
	elif line.startswith("$ cd "):
		folder_name = line[5:]
		if folder_name not in current:
			current[folder_name] = {}
		folder = current[folder_name]
		path.append(current)
		current = folder
	elif line == "$ ls":
		pass
	else:
		words = line.split()
		name = ''.join(words[1:])
		if words[0] == "dir":
			node = {}
		else:
			size = int(words[0])
			node = size
		current[name] = node

	index += 1

s = 0
count_size(filesystem)

print(s)
