import sys

numbers = [int(x.strip()) for x in sys.stdin]

for i in range(25, len(numbers)):
	n = numbers[i]
	prev_numbers = numbers[i - 25:i]
	found = False
	for j, n1 in enumerate(prev_numbers):
		for n2 in prev_numbers[j + 1:]:
			if n1 + n2 == n:
				found = True
				break
		if found:
			break
	if not found:
		print(n)
		break
