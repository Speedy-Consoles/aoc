import sys
from itertools import islice

class Element(object):
	def __init__(self, number):
		self.number = number

elements = [Element(int(line)) for line in sys.stdin.read().splitlines()]
num_elements = len(elements)

zero = next(element for element in elements if element.number == 0)

for i, element in enumerate(elements):
	element.prev = elements[i - 1]
	element.next = elements[(i + 1) % num_elements]

for element in elements:
	element.prev.next = element.next
	element.next.prev = element.prev
	for i in range(element.number % (num_elements - 1)):
		element.next = element.next.next
	element.prev = element.next.prev
	element.next.prev = element
	element.prev.next = element

s = 0
current = zero
for i in range(3001):
	if i in (1000, 2000, 3000):
		s += current.number
	current = current.next

print(s)
