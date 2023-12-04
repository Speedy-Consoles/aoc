import sys
import re

def in_range_check(a, b):
	return lambda x: int(x) >= a and int(x) <= b

def height_check(x):
	match = re.search('^([0-9]+)(cm|in)$', x)
	if match is None:
		return False
	number = int(match.group(1))
	unit = match.group(2)
	if unit == 'cm':
		return number >= 150 and number <= 193
	else:
		return number >=59 and number <= 76

eye_colors = {
	'amb',
	'blu',
	'brn',
	'gry',
	'grn',
	'hzl',
	'oth',
}

required_keys = [
    ('byr', in_range_check(1920, 2002)),
    ('iyr', in_range_check(2010, 2020)),
    ('eyr', in_range_check(2020, 2030)),
    ('hgt', lambda x: height_check(x)),
    ('hcl', lambda x: re.search('^#[0-9a-f]{6}$', x) is not None),
    ('ecl', lambda x: x in eye_colors),
    ('pid', lambda x: re.search('^[0-9]{9}$', x) is not None),
    #('cid', lambda x: True),
]

passports = sys.stdin.read().split('\n\n')

valid_count = 0
for passport in passports:
	items = passport.split()
	item_map = dict(item.split(':') for item in items)
	if all(key in item_map and check(item_map[key]) for key, check in required_keys):
		valid_count += 1

print(valid_count)
