total = 0
try:
	while True:
		total += int(input())//3-2
except EOFError:
	print(total)
