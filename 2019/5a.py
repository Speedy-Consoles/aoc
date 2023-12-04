import sys

class IntcodeProgramException(Exception):
	pass

class Operation:
	def __init__(self, num_in_params, has_out_param, f):
		self.num_in_params = num_in_params
		self.has_out_param = has_out_param
		self.do = f

OPERATIONS = {
	1: Operation(2, True, lambda p, i: (p[0] + p[1], None)),
	2: Operation(2, True, lambda p, i: (p[0] * p[1], None)),
	3: Operation(0, True, lambda p, i: (i(), None)),
	4: Operation(1, False, lambda p, i: (None, p[0])),
}

class IntcodeComputer:
	def __init__(self, mem, inpt):
		self.mem = mem
		self.input = inpt
		self.pc = 0

	def run_program(self):
		while True:
			try:
				opcode = self.mem[self.pc] % 100
				if opcode == 99:
					return
				self.modes = self.mem[self.pc] // 100

				try:
					operation = OPERATIONS[opcode]
				except KeyError:
					raise IntcodeProgramException('Invalid opcode at {} ({})!'.format(self.pc, opcode))

				num_in_params = operation.num_in_params
				in_params = [self._get_in_param(i) for i in range(num_in_params)]
				result, output = operation.do(in_params, self.input)
				if output is not None:
					yield output
				self.pc += 1 + num_in_params
				if operation.has_out_param:
					self.mem[self.mem[self.pc]] = result
					self.pc += 1
			except IndexError:
				raise IntcodeProgramException('Memory error!')


	def _get_in_param(self, index):
		mode = (self.modes // 10**index) % 10
		operand = self.mem[self.pc + 1 + index]
		if mode == 0:
			return self.mem[operand]
		elif mode == 1:
			return operand
		else:
			raise IntcodeProgramException('Invalid parameter mode at {} ({})!'.format(self.pc, mode))

def one():
	return 1

mem = [int(x) for x in input().split(',')]

computer = IntcodeComputer(mem, one)
for output in computer.run_program():
	print(output)

