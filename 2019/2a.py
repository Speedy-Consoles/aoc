import sys

numbers = [int(x) for x in input().split(',')]
numbers[1] = 12
numbers[2] = 2

pc = 0
while True:
	opcode = numbers[pc]
	if opcode == 99:
		break
	if opcode not in [1, 2]:
		print("Invalid opcode!")
		sys.exit(1)

	operand1 = numbers[numbers[pc + 1]]
	operand2 = numbers[numbers[pc + 2]]
	target_address = numbers[pc + 3]
	if opcode == 1:
		numbers[target_address] = operand1 + operand2
	else:
		numbers[target_address] = operand1 * operand2
	pc += 4

print(numbers[0])
