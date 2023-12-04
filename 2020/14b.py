import sys
import re

mask_re = re.compile('^mask = ([X01]{36})$')
assignment_re = re.compile('^mem\\[([0-9]+)\\] = ([0-9]+)$')

mem = {}
for line in sys.stdin:
	if line.startswith('mask'):
		mask_string = mask_re.search(line.strip()).group(1)
		floating_indices = [i for i, c in enumerate(reversed(mask_string)) if c == 'X']
		and_mask = int(''.join(str(int(c == '0')) for c in mask_string), 2)
		base_or_mask = int(''.join(str(int(c == '1')) for c in mask_string), 2)
	else:
		match = assignment_re.search(line.strip())
		address = int(match.group(1))
		value = int(match.group(2))
		for floating_bits in range(1 << len(floating_indices)):
			or_mask = base_or_mask
			for i, index in enumerate(floating_indices):
				or_mask |= ((floating_bits >> i) & 1) << index
			mem[(address & and_mask) | or_mask] = value

print(sum(mem.values()))
