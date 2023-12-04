import sys
import re

mask_re = re.compile('^mask = ([X01]{36})$')
assignment_re = re.compile('^mem\\[([0-9]+)\\] = ([0-9]+)$')


def apply_mask(num):
	return (num & and_mask) | or_mask

mem = {}
for line in sys.stdin:
	if line.startswith('mask'):
		mask_string = mask_re.search(line.strip()).group(1)
		and_mask = int(''.join(str(int(c == 'X')) for c in mask_string), 2)
		or_mask =  int(''.join(str(int(c == '1')) for c in mask_string), 2)
	else:
		match = assignment_re.search(line.strip())
		address = int(match.group(1))
		value = int(match.group(2))
		mem[address] = apply_mask(value)

print(sum(mem.values()))
