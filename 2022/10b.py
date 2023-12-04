import sys

lines = iter(sys.stdin.read().splitlines())

add = None
register = 1
for y in range(6):
	for x in range(40):
		print('#' if x >= register - 1 and x <= register + 1 else ' ', end='')
		if add is not None:
			register += add
			add = None
		else:
			try:
				line = next(lines)
				if line.startswith('addx '):
					add = int(line[5:])
				elif line == 'noop':
					add = None
				else:
					raise Exception('Whaaaat?')
			except StopIteration:
				add = 0
	print()
