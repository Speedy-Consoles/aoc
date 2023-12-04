import itertools
import collections

class IntcodeProgramException(Exception):
	pass

class Memory:
	def __init__(self, initial_memory):
		self.lmem = initial_memory
		self.dmem = {}

	def _get_mem_block(self, index):
		if index < 0:
			raise IndexError('Negative memory access')
		elif index < len(self.lmem):
			return self.lmem
		else:
			return self.dmem

	def __getitem__(self, index):
		return self._get_mem_block(index)[index]

	def __setitem__(self, index, value):
		self._get_mem_block(index)[index] = value

	def __delitem__(self, index, value):
		del self._get_mem_block(index)[index]

class Operation:
	def __init__(self, num_in_params, f):
		self.num_in_params = num_in_params
		self.do = f

OPERATIONS = {
	1: Operation(2, lambda p, i, b: (p[0] + p[1],              None, None,                        None)),
	2: Operation(2, lambda p, i, b: (p[0] * p[1],              None, None,                        None)),
	3: Operation(0, lambda p, i, b: (i.__next__(),             None, None,                        None)),
	4: Operation(1, lambda p, i, b: (None,                     p[0], None,                        None)),
	5: Operation(2, lambda p, i, b: (None,                     None, p[1] if p[0] != 0 else None, None)),
	6: Operation(2, lambda p, i, b: (None,                     None, p[1] if p[0] == 0 else None, None)),
	7: Operation(2, lambda p, i, b: (1 if p[0] < p[1] else 0,  None, None,                        None)),
	8: Operation(2, lambda p, i, b: (1 if p[0] == p[1] else 0, None, None,                        None)),
	9: Operation(1, lambda p, i, b: (None,                     None, None,                        b + p[0])),
}

class IntcodeComputer:
	def __init__(self, mem, input_iterator=None):
		self.mem = Memory(mem)
		self.pc = 0
		self.rb = 0
		self.input_iterator = input_iterator

	def run(self):
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
				in_params = [self._get_param(i, 'in') for i in range(num_in_params)]

				# execute instruction
				try:
					result, output, new_pc, new_rb = operation.do(in_params, self.input_iterator, self.rb)
				except StopIteration:
					raise IntcodeProgramException('Not enough input values!')

				# output
				if output is not None:
					yield output

				# move the relative base
				if new_rb is not None:
					self.rb = new_rb

				# store result and increase the program counter
				if result is not None:
					self.mem[self._get_param(num_in_params, 'out')] = result
					self.pc += 2 + num_in_params
				else:
					self.pc += 1 + num_in_params
			except IndexError:
				raise IntcodeProgramException('Memory error during execution of operation at {}!'.format(self.pc))

			# set new program counter
			if new_pc is not None:
				self.pc = new_pc

	def set_input(self, input_iterator):
		self.input_iterator = input_iterator

	def _get_param(self, index, direction):
		mode = (self.modes // 10**index) % 10
		operand = self.mem[self.pc + 1 + index]

		if mode == 0:
			address = operand
		elif mode == 1 and direction == 'in':
			return operand
		elif mode == 2:
			address = operand + self.rb
		else:
			raise IntcodeProgramException('Invalid parameter mode at {} ({})!'.format(self.pc, mode))

		if direction == 'in':
			return self.mem[address]
		return address

class DynamicIterator:
	def __init__(self):
		self.queue = collections.deque()

	def put(self, item):
		self.queue.append(item)

	def __iter__(self):
		return self

	def __next__(self):
		if len(self.queue) == 0:
			raise StopIteration()
		return self.queue.popleft()

initial_mem = [int(x) for x in input().split(',')]
computer = IntcodeComputer(initial_mem, iter([2]))
for output in computer.run():
	print(output)

