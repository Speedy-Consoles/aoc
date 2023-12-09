import sys

def parse_line(line):
	return [int(x) for x in line.split()]

def derive(seq):
	return [b - a for a, b in zip(seq, seq[1:])]

def extend(seq):
	return [0 if all(x == 0 for x in seq) else seq[0] - extend(derive(seq))[0]] + seq

sequences = map(parse_line, sys.stdin.read().splitlines())
print(sum(extend(sequence)[0] for sequence in sequences))
