import sys
import math

asteroids = []
for y, line in enumerate(sys.stdin):
	for x, c in enumerate(line):
		if c == '#':
			asteroids.append((x, y))
num = len(asteroids)

uds = {a: {} for a in asteroids}
for a in asteroids:
	for b in asteroids:
		if a == b:
			continue
		df = (b[0] - a[0], b[1] - a[1])
		gcd = math.gcd(df[0], df[1])
		d = ( df[0] // gcd,  df[1] // gcd)
		if d in uds[a]:
			uds[a][d].append(b)
		else:
			uds[a][d] = [b]

station, dir_asteroids = max(uds.items(), key=lambda x: len(x[1]))

for da in dir_asteroids.values():
	da[:] = sorted(da, key=lambda x: abs(x[0]), reverse=True)

sorted_directions = sorted(dir_asteroids, key=lambda x: math.atan2(x[0], x[1]), reverse=True)

counter = 0
while True:
	for sd in sorted_directions:
		das = dir_asteroids[sd]
		if len(das) == 0:
			continue
		a = das.pop()
		counter += 1
		if counter == 200:
			print(a[0] * 100 + a[1])
			sys.exit(0)
