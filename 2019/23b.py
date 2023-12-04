import itertools
import collections
import math
import sys

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
	1: Operation('ADD', 2, lambda p, b: (p[0] + p[1],              None, None,                        None)),
	2: Operation('MUL', 2, lambda p, b: (p[0] * p[1],              None, None,                        None)),
	3: Operation('IN',  0, lambda p, b: (None,                     'in', None,                        None)),
	4: Operation('OUT', 1, lambda p, b: (None,                     p[0], None,                        None)),
	5: Operation('JIT', 2, lambda p, b: (None,                     None, p[1] if p[0] != 0 else None, None)),
	6: Operation('JIF', 2, lambda p, b: (None,                     None, p[1] if p[0] == 0 else None, None)),
	7: Operation('LT',  2, lambda p, b: (1 if p[0] < p[1] else 0,  None, None,                        None)),
	8: Operation('EQ',  2, lambda p, b: (1 if p[0] == p[1] else 0, None, None,                        None)),
	9: Operation('ARB', 1, lambda p, b: (None,                     None, None,                        b + p[0])),
}

class IntcodeComputer:
	def __init__(self, mem):
		self.mem = Memory(mem)
		self.pc = 0
		self.rb = 0

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
					result, output, new_pc, new_rb = operation.do(in_params, self.rb)
					dprint('Result:', result)
					dprint('Output:', output)
					dprint('New program counter:', new_pc)
					dprint('New relative base:', new_rb)
				except StopIteration:
					raise IntcodeProgramException('Not enough input values!')

				# output
				if output is not None:
					result = yield output

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


mem = [int(x) for x in input().split(',')]
generators = []
queues = []
for i in range(50):
	c = IntcodeComputer(mem[:])
	generators.append(c.run())
	queues.append(collections.deque([i]))

finished = set()
waiting = set()
nat_x = None
nat_y = None
sent_nat_ys = set()
while True:
	idle_counter = 0
	for i in range(50):
		if i in finished:
			continue
		g = generators[i]
		payload = None
		if i in waiting:
			waiting.remove(i)
			if len(queues[i]) > 0:
				payload = queues[i].popleft()
			else:
				payload = -1

		try:
			out = g.send(payload)
		except StopIteration:
			finished.add(i)
			continue

		if out == 'in':
			if payload == -1:
				idle_counter += 1
			waiting.add(i)
		else:
			addr = out
			x = next(g)
			y = next(g)
			if addr == 255:
				nat_x = x
				nat_y = y
			else:
				queues[addr].append(x)
				queues[addr].append(y)
	if idle_counter == 50:
		if nat_x is None:
			raise Exception('nat_x is None!')
		if nat_y in sent_nat_ys:
			print(nat_y)
			sys.exit()
		sent_nat_ys.add(nat_y)
		queues[0].append(nat_x)
		queues[0].append(nat_y)		

