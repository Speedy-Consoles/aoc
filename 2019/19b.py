import itertools
import collections
import math

DEBUG = False

def dprint(*args):
	if DEBUG:
		print(*args)

class IntcodeProgramException(Exception):
	pass

class Memory:
	def __init__(self, initial_memory):
		self.lmem = initial_memory
		self.dmem = collections.defaultdict(lambda: 0)

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
	def __init__(self, name, num_in_params, f):
		self.name = name
		self.num_in_params = num_in_params
		self.do = f

	def __str__(self):
		return self.name

OPERATIONS = {
	1: Operation('ADD', 2, lambda p, i, b: (p[0] + p[1],              None, None,                        None)),
	2: Operation('MUL', 2, lambda p, i, b: (p[0] * p[1],              None, None,                        None)),
	3: Operation('IN',  0, lambda p, i, b: (int(next(i)),             None, None,                        None)),
	4: Operation('OUT', 1, lambda p, i, b: (None,                     p[0], None,                        None)),
	5: Operation('JIT', 2, lambda p, i, b: (None,                     None, p[1] if p[0] != 0 else None, None)),
	6: Operation('JIF', 2, lambda p, i, b: (None,                     None, p[1] if p[0] == 0 else None, None)),
	7: Operation('LT',  2, lambda p, i, b: (1 if p[0] < p[1] else 0,  None, None,                        None)),
	8: Operation('EQ',  2, lambda p, i, b: (1 if p[0] == p[1] else 0, None, None,                        None)),
	9: Operation('ARB', 1, lambda p, i, b: (None,                     None, None,                        b + p[0])),
}

class IntcodeComputer:
	def __init__(self, mem, input_iterator=None):
		self.mem = Memory(mem)
		self.pc = 0
		self.rb = 0
		self.input_iterator = iter(input_iterator)

	def run(self):
		while True:
			try:
				dprint('Instruction Integer at {}: {}'.format(self.pc, self.mem[self.pc]))
				
				# fetch instruction
				opcode = self.mem[self.pc] % 100
				dprint('Opcode:', opcode)
				if opcode == 99:
					return

				# get operation
				try:
					operation = OPERATIONS[opcode]
					dprint('Operation:', operation)
				except KeyError:
					raise IntcodeProgramException('Invalid opcode at {} ({})!'.format(self.pc, opcode))

				# fetch parameters
				self.modes = self.mem[self.pc] // 100
				dprint('Modes:', self.modes)
				num_in_params = operation.num_in_params
				in_params = [self._get_param(i, 'in') for i in range(num_in_params)]
				dprint('Input parameters:', in_params)

				# execute instruction
				try:
					result, output, new_pc, new_rb = operation.do(in_params, self.input_iterator, self.rb)
					dprint('Result:', result)
					dprint('Output:', output)
					dprint('New program counter:', new_pc)
					dprint('New relative base:', new_rb)
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
					result_address = self._get_param(num_in_params, 'out')
					dprint('Result address:', result_address)
					self.mem[result_address] = result
			except IndexError:
				raise IntcodeProgramException('Memory error during execution of operation at {}!'.format(self.pc))

			# set new program counter
			if new_pc is not None:
				self.pc = new_pc
			elif result is not None:
				self.pc += 2 + num_in_params
			else:
				self.pc += 1 + num_in_params

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

def iter_coords():
	for ystart in itertools.count():
		for x in range(ystart + 1):
			yield (x, ystart - x)

def check_fit(pos):
	for y in range(pos[1], pos[1] + 100):
		for x in range(pos[0], pos[0] + 100):
			if not get_field((x, y)):
				return False
	return True

board = {}
def get_field(pos):
	if pos in board:
		return board[pos]
	else:
		computer = IntcodeComputer(mem[:], pos)
		result = next(computer.run()) == 1
		board[pos] = result
		return result

mem = [int(x) for x in input().split(',')]

s = 0
for pos in iter_coords():
	if check_fit(pos):
		print(pos[0] * 10000 + pos[1])
		break

