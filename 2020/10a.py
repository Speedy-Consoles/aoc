import sys
from collections import Counter

joltages = sorted(int(s.strip()) for s in sys.stdin)
joltages = [0] + joltages + [joltages[-1] + 3]
differences = [joltages[i] - joltages[i - 1] for i in range(1, len(joltages))]

histogram = Counter(differences)
print(histogram[1] * histogram[3])
