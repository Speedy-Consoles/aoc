import sys
import math

asteroids = []
for y, line in enumerate(sys.stdin):
	for x, c in enumerate(line):
		if c == '#':
			asteroids.append((x, y))
num = len(asteroids)

uds = [set() for i in range(num)]
for i in range(num):
	for j in range(i + 1, num):
		a = asteroids[i]
		b = asteroids[j]
		d = (b[0] - a[0], b[1] - a[1])
		gcd = math.gcd(d[0], d[1])
		uds[i].add((d[0] // gcd, d[1] // gcd))
		uds[j].add((-d[0] // gcd, -d[1] // gcd))

print(max(len(x) for x in uds))
