import sys
import re

required_keys = [
    'byr',
    'iyr',
    'eyr',
    'hgt',
    'hcl',
    'ecl',
    'pid',
    #'cid',
]

passports = sys.stdin.read().split('\n\n')

valid_count = 0
for passport in passports:
	items = passport.split()
	keys = set(item.split(':')[0] for item in items)
	if all(key in keys for key in required_keys):
		valid_count += 1

print(valid_count)
