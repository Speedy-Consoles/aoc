import sys

line = sys.stdin.read()
print(next(i for i in range(14, len(line) + 1) if len(set(line[i-14:i])) == 14))
