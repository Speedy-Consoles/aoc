total = 0
try:
	while True:
		mass = int(input())
		while mass != 0:
			mass = max(0, mass // 3 - 2)
			total += mass
except EOFError:
	print(total)
