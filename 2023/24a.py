import sys
import re
from dataclasses import dataclass

PATTERN = re.compile(r'^(-?\d+), +(-?\d+), +(-?\d+) +@ +(-?\d+), +(-?\d+), +(-?\d+)$')

@dataclass
class Hailstone:
	px: int
	py: int
	pz: int
	vx: int
	vy: int
	vz: int

RANGE = range(200000000000000, 400000000000001)

def parse_line(s):
	return Hailstone(*map(int, PATTERN.match(s).groups()))

def check(h1, h2):
	if h2.vx != 0:
		slope = h2.vy / h2.vx
		nominator = h2.py - h1.py + slope * (h1.px - h2.px)
		denominator = h1.vy - slope * h1.vx
	else:
		slope = h2.vx / h2.vy
		nominator = h2.px - h1.px + slope * (h1.py - h2.py)
		denominator = h1.vx - slope * h1.vy

	if denominator == 0:
		return False

	t1 = nominator / denominator

	if h2.vx != 0:
		t2 = (h1.px - h2.px + h1.vx * t1) / h2.vx
	else:
		t2 = (h1.py - h2.py + h1.vy * t1) / h2.vy

	if t1 < 0 or t2 < 0:
		return False

	x = h1.px + h1.vx * t1
	y = h1.py + h1.vy * t1

	return all(v >= RANGE.start and v < RANGE.stop for v in (x, y))

hailstones = list(map(parse_line, sys.stdin.read().splitlines()))

print(sum(check(h1, h2) for i, h1 in enumerate(hailstones) for h2 in hailstones[i + 1:]))
