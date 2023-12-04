import sys

x = 1
s = 0
iteration = 1
for line in sys.stdin.read().splitlines():
	if (iteration + 20) % 40 == 0 and iteration <= 220:
		s += iteration * x

	if line.startswith('addx '):
		iteration += 1
		if (iteration + 20) % 40 == 0 and iteration <= 220:
			s += iteration * x
		iteration += 1
		x += int(line[5:])
	elif line == 'noop':
		iteration += 1
	else:
		raise Exception('Whaaaat?')

while iteration <= 220:
	if (iteration + 20) % 40 == 0:
		s += iteration * x
	iteration += 1

print(s)
