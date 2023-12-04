import sys

table = {
	')': ('(', 3),
	']': ('[', 57),
	'}': ('{', 1197),
	'>': ('<', 25137),
}

score = 0
for line in sys.stdin.read().splitlines():
	stack = []
	for c in line:
		if c in '([{<':
			stack.append(c)
		else:
			expected, points = table[c]
			if len(stack) == 0 or stack.pop() != expected:
				score += points
				break

print(score)
