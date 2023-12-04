import sys

pairs = ((ord(x[0]) - ord('A'), ord(x[2]) - ord('X')) for x in sys.stdin.read().splitlines())
scores = (b * 3 + ((a + b - 1 + 3) % 3) + 1 for a, b in pairs)

print(sum(scores))

