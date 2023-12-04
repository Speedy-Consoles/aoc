import sys
import re

PATTERN = re.compile('^move (\\d+) from (\\d+) to (\\d+)$')

stacks_text, instructions_text = sys.stdin.read().split('\n\n')
stacks_lines = stacks_text.splitlines()[:-1]
n = (len(stacks_lines[0]) + 1) // 4

stacks = [[] for i in range(n)]
for line in reversed(stacks_lines):
	for i in range(n):
		crate_char = line[1 + i * 4]
		if crate_char != ' ':
			stacks[i].append(crate_char)

for line in instructions_text.splitlines():
	amount, src, dst = map(int, PATTERN.match(line).groups())
	moved = stacks[src - 1][-amount:]
	stacks[dst - 1] += moved
	del stacks[src - 1][-amount:]

print(''.join(stack[-1] for stack in stacks))
