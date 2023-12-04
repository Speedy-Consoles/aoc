import sys
from collections import Counter

groups = sys.stdin.read().split('\n\n')
counter = 0
for group in groups:
	size = group.count('\n') + 1
	answers = dict(Counter(group))
	counter += sum(1 for count in answers.values() if count == size)

print(counter)
