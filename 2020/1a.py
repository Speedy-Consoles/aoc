import sys

numbers = [int(s) for s in sys.stdin]
for a in numbers:
	for b in numbers:
		if a + b == 2020:
			print(a * b)
			sys.exit(0)
sys.exit(1)
