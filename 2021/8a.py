import sys

count = 0
for line in sys.stdin.read().splitlines():
	split = line.split(' | ')
	unique_patterns = split[0].split()
	output_patterns = split[1].split()

	count += sum(int(len(p) in {2, 3, 4, 7}) for p in output_patterns)

print(count)
