import sys

def prio(a):
	return ord(a) - ord('a') + 1 if a.islower() else ord(a) - ord('A') + 27

def grouped(l, n):
	return (l[i:i+n] for i in range(0, len(l), n))

print(sum(prio((set(group[0]) & set(group[1]) & set(group[2])).pop()) for group in grouped(sys.stdin.read().splitlines(), 3)))

