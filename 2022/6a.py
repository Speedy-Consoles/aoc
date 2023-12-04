import sys

line = sys.stdin.read()
print(next(i for i in range(4, len(line) + 1) if len(set(line[i-4:i])) == 4))
