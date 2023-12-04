numbers = [int(x) for x in input().split(',')]
seen = {}
for i, number in enumerate(numbers[:-1]):
	seen[int(number)] = i
last_number = numbers[-1]

for i in range(len(numbers), 30000000):
	if last_number in seen:
		number = i - seen[last_number] - 1
	else:
		number = 0
	seen[last_number] = i - 1
	last_number = number

print(number)
