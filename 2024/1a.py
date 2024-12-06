import sys

print(sum(abs(a - b) for a, b in zip(*map(sorted, zip(*([int(s) for s in p.split()] for p in sys.stdin.readlines()))))))
