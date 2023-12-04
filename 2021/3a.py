import sys

lines = sys.stdin.read().splitlines()
num_bits = len(lines[0])
numbers = [int(x, 2) for x in lines]

gamma_rate = 0
epsilon_rate = 0
for i in range(num_bits):
	count = sum(((number >> i) & 1) for number in numbers)
	assert(count != len(numbers))
	bit = int(count > len(numbers) / 2)
	gamma_rate |= bit << i
	epsilon_rate |= (1 - bit) << i

print(gamma_rate * epsilon_rate)
