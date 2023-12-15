from functools import reduce

def hash(s):
	return reduce(lambda h, c: (h + ord(c)) * 17 % 256, s, 0)

print(sum(map(hash, input().split(','))))
