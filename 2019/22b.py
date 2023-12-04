import sys

INTO_NEW = 'deal into new stack'
CUT = 'cut '
INCREMENT = 'deal with increment '

def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)
		return (g, x - (b // a) * y, y)

def modinv(a, m):
	g, x, y = egcd(a, m)
	if g != 1:
		raise Exception('Modular inverse does not exist!', a, m)
	else:
		return x % m

class Permutation:
	def __init__(self, n):
		self.offset = 0
		self.factor = 1
		self.n = n

	def reverse(self):
		self.factor = (-self.factor) % self.n
		self.offset = (-self.offset - 1) % self.n

	def scale(self, factor):
		self.factor = (self.factor * factor) % self.n
		self.offset = (self.offset * factor) % self.n

	def shift(self, offset):
		self.offset = (self.offset - offset) % self.n

	def repeat(self, times):
		a = self.factor
		n = self.n
		b = self.offset
		a_n = pow(a, times, n)
		self.offset = (b * (a_n - 1) * modinv(a - 1, n)) % n
		self.factor = a_n

	def permute(self, index):
		return (index * self.factor + self.offset) % self.n

	def at(self, index):
		return ((index - self.offset) * modinv(self.factor, self.n)) % self.n

	def as_list(self):
		return [self.at(x) for x in range(self.n)]

length = 119315717514047
num_repetitions = 101741582076661
input_string = sys.stdin.read()

p = Permutation(length)
for line in input_string.strip().split('\n'):
	if line == INTO_NEW:
		p.reverse()
	elif line.startswith(CUT):
		cut_index = int(line[len(CUT):])
		p.shift(cut_index)
	elif line.startswith(INCREMENT):
		increment = int(line[len(INCREMENT):])
		p.scale(increment)
	else:
		raise Exception('Invalid shuffle:', line)

p.repeat(num_repetitions)
print(p.at(2020))
