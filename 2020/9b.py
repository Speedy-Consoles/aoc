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
		result = n
		break

if found:
	print('ERROR')
	sys.exit(1)

cum_sum = [0] * (len(numbers) + 1)
for i, n in enumerate(numbers):
	cum_sum[i + 1] = cum_sum[i] + n

for i in range(len(cum_sum)):
	for j in range(i + 2, len(cum_sum)):
		if cum_sum[j] - cum_sum[i] == result:
			print(min(numbers[i:j]) + max(numbers[i:j]))
