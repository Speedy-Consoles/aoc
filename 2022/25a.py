import sys

DIGITS = {
	'2': 2,
	'1': 1,
	'0': 0,
	'-': -1,
	'=': -2,
}
REV_DIGITS = {b: a for a, b in DIGITS.items()}
	
number = sum(sum(5**i * DIGITS[x] for i, x in enumerate(reversed(line))) for line in sys.stdin.read().splitlines())

snafu = ''
power = 1
while number > 0:
	rest = number % 5
	if rest <= 2:
		digit = str(rest)
	else:
		digit = REV_DIGITS[rest - 5]
		number += 5
	snafu = digit + snafu
	number //= 5
print(snafu)
