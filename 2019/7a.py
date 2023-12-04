import itertools

class IntcodeProgramException(Exception):
	pass

class Operation:
	def __init__(self, num_in_params, f):
		self.num_in_params = num_in_params
		self.do = f

OPERATIONS = {
	1: Operation(2, lambda p, i: (p[0] + p[1],              None, None)),
	2: Operation(2, lambda p, i: (p[0] * p[1],              None, None)),
	3: Operation(0, lambda p, i: (i.__next__(),             None, None)),
	4: Operation(1, lambda p, i: (None,                     p[0], None)),
	5: Operation(2, lambda p, i: (None,                     None, p[1] if p[0] != 0 else None)),
	6: Operation(2, lambda p, i: (None,                     None, p[1] if p[0] == 0 else None)),
	7: Operation(2, lambda p, i: (1 if p[0] < p[1] else 0,  None, None)),
	8: Operation(2, lambda p, i: (1 if p[0] == p[1] else 0, None, None)),
}

class IntcodeComputer:
	def __init__(self, mem, input_iterator):
		self.mem = mem
		self.input_iterator = input_iterator
		self.pc = 0

	def run_program(self):
		while True:
			try:
				# fetch instruction
				opcode = self.mem[self.pc] % 100
				if opcode == 99:
					return

				# get operation
				try:
					operation = OPERATIONS[opcode]
				except KeyError:
					raise IntcodeProgramException('Invalid opcode at {} ({})!'.format(self.pc, opcode))

				# fetch parameters
				self.modes = self.mem[self.pc] // 100
				num_in_params = operation.num_in_params
				in_params = [self._get_in_param(i) for i in range(num_in_params)]

				# execute instruction
				try:
					result, output, new_pc = operation.do(in_params, self.input_iterator)
				except StopIteration:
					raise IntcodeProgramException('Not enough input values!')

				# output
				if output is not None:
					yield output

				# store result and increase the program counter
				self.pc += 1 + num_in_params
				if result is not None:
					self.mem[self.mem[self.pc]] = result
					self.pc += 1
			except IndexError:
				raise IntcodeProgramException('Memory error during execution of operation at {}!'.format(self.pc))

			# set new program counter
			if new_pc is not None:
				self.pc = new_pc

	def _get_in_param(self, index):
		mode = (self.modes // 10**index) % 10
		operand = self.mem[self.pc + 1 + index]
		if mode == 0:
			return self.mem[operand]
		elif mode == 1:
			return operand
		else:
			raise IntcodeProgramException('Invalid parameter mode at {} ({})!'.format(self.pc, mode))

def compute_amp_out(initial_mem, phase_settings):
	amp_in_out = 0
	for ai in range(5):
		computer = IntcodeComputer(initial_mem[:], (phase_settings[ai], amp_in_out).__iter__())
		amp_in_out = computer.run_program().__next__()
	return amp_in_out

initial_mem = [int(x) for x in input().split(',')]
print(max(compute_amp_out(initial_mem, phase_settings) for phase_settings in itertools.permutations(range(5))))

