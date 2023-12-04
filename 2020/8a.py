import sys

program = []
for line in sys.stdin:
	parts = line.strip().split(' ')
	command = parts[0]
	argument = int(parts[1])
	program.append((command, argument))

pc = 0
acc = 0
executed_lines = set()
while True:
	if pc in executed_lines:
		break

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

print(acc)
