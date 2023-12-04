import subprocess
import itertools

jump_examples = [
	'.########',
	'#..#.####',
	'.#..#####',
	'##.#..###',
	'##.#..##.',
	'#.##...#.',
	'##.#.#.#.',
]

walk_examples = [
	'####..#.#',
	'##...####',
	'###.#####',
	'#...#####',
	'####.####',
	'##.#.#...',
	'##.#.##..',
	'##..#.###',
	'##..####.',
]

min_terms = [int(''.join('1' if x == '#' else '0' for x in e)[::-1], 2) for e in jump_examples]
s = set(x for x in range(2**9))
for e in itertools.chain(walk_examples, jump_examples):
	s.discard(int(''.join('1' if x == '#' else '0' for x in e)[::-1], 2))
dc_terms = list(s)

command = 'python2 qm_py2_helper.py {} {}'.format(
	','.join(str(x) for x in min_terms),
	','.join(str(x) for x in dc_terms)
)

process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
output, error = process.communicate()
print(output.decode('utf-8'))
