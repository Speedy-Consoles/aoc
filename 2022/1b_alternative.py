import sys

elves = sys.stdin.read().split('\n\n')
sums = (sum(int(lines) for lines in elf.splitlines()) for elf in elves)
print(sum(sorted(sums)[-3:]))
