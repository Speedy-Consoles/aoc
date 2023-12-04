import sys

opening = {
	'(': ')',
	'[': ']',
	'{': '}',
	'<': '>',
}

points = {
	')': 1,
	']': 2,
	'}': 3,
	'>': 4,
}

scores = []
for line in sys.stdin.read().splitlines():
	stack = []
	corrupt = False
	for c in line:
		if c in opening:
			stack.append(opening[c])
		else:
			if len(stack) == 0 or c != stack.pop():
				corrupt = True
				break
	if not corrupt:
		scores.append(sum(5**i * points[c] for i, c in enumerate(stack)))

print(sorted(scores)[len(scores) // 2])
