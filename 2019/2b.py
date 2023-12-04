import sys

class IntcodeProgramException(Exception):
	pass

def run_program(program):
	pc = 0
	while True:
		opcode = program[pc]
		if opcode == 99:
			return
		if opcode not in [1, 2]:
			raise IntcodeProgramException('Invalid opcode at {} ({})!'.format(pc, opcode))

		try:
			operand1 = program[program[pc + 1]]
			operand2 = program[program[pc + 2]]
			result_address = program[pc + 3]
			if opcode == 1:
				program[result_address] = operand1 + operand2
			else:
				program[result_address] = operand1 * operand2
		except IndexError:
			raise IntcodeProgramException('Malformed program!')

		pc += 4

initial_program = [int(x) for x in input().split(',')]

for i in range(10000):
	program = initial_program[:]

	noun = i // 100
	verb = i % 100

	program[1] = noun
	program[2] = verb

	try:
		run_program(program)
	except IntcodeProgramException as e:
		print('{}, {}: {}'.format(noun, verb, str(e)))
		continue

	if program[0] == 19690720:
		print('100 * {} + {} = {}'.format(noun, verb, 100 * noun + verb))
		sys.exit()

print('No valid solution found!')
