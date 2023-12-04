import sys

numbers = [int(s) for s in sys.stdin]
for a in numbers:
	for b in numbers:
		for c in numbers:
			if a + b + c == 2020:
				print(a * b * c)
				sys.exit(0)
sys.exit(1)
