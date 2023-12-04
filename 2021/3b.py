import sys

def find_number(numbers, num_bits, get_bit):
	index = num_bits - 1
	while len(numbers) > 1:
		assert(index >= 0)
		count = sum(((number >> index) & 1) for number in numbers)
		bit = get_bit(int(count >= len(numbers) / 2))
		numbers = list(filter(lambda number: (number >> index) & 1 == bit, numbers))
		index -= 1
	assert(len(numbers) == 1)
	return numbers[0]

lines = sys.stdin.read().splitlines()
num_bits = len(lines[0])
numbers = [int(x, 2) for x in lines]

oxygen_generator_rate = find_number(numbers, num_bits, lambda bit: bit)
co2_scrubber_rate = find_number(numbers, num_bits, lambda bit: 1 - bit)

print(oxygen_generator_rate * co2_scrubber_rate)
