import sys

def test_program(program):
	pc = 0
	acc = 0
	executed_lines = set()
	while True:
		if pc == len(program):
			return acc
		elif pc < 0 or pc > len(program) or pc in executed_lines:
			return None

		command = program[pc][0]
		argument = program[pc][1]

		executed_lines.add(pc)

		if command == 'acc':
			acc += argument
			pc += 1
		elif command == 'jmp':
			pc += argument
		elif command == 'nop':
			pc += 1
		else:
			print('ERROR')
			sys.exit(1)

program = []
for line in sys.stdin:
	parts = line.strip().split(' ')
	command = parts[0]
	argument = int(parts[1])
	program.append([command, argument])


for i in range(len(program)):
	command = program[i][0]
	if command != 'acc':
		if command == 'nop':
			program[i][0] = 'jmp'
			old = 'nop'
		elif command == 'jmp':
			program[i][0] = 'nop'
			old = 'jmp'
		else:
			print('ERROR')
			sys.exit(1)

		result = test_program(program)
		if result is not None:
			print(result)
			sys.exit(0)
		program[i][0] = old

