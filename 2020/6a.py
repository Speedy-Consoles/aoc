import sys

groups = sys.stdin.read().split('\n\n')
num_yesses = (len(set(group.replace('\n', ''))) for group in groups)
print(sum(num_yesses))
