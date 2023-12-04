import sys
import math

input()

offset = 0
period = 1
for i, x in enumerate(input().split(',')):
	if x != 'x':
		bus = int(x)
		offset += period * ((pow(period, -1, bus) * (-offset - i)) % bus)
		period = math.lcm(period, bus)

print(offset)
