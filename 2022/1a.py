import sys

elves = sys.stdin.read().split('\n\n')
sums = (sum(int(lines) for lines in elf.splitlines()) for elf in elves)

print(max(sums))

