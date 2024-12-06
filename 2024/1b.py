import sys
from collections import Counter

a, b = zip(*([int(s) for s in p.split()] for p in sys.stdin.readlines()))
c = Counter(b)
print(sum(x * c[x] for x in a))
