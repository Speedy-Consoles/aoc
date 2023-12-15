import re
from functools import reduce

PATTERN = re.compile(r'^([a-z]+)(?:(-)|(=)(\d))$')

def hash(s):
	return reduce(lambda h, c: (h + ord(c)) * 17 % 256, s, 0)

instructions = input().split(',')
focal_lengths = {}
boxes = [[] for _ in range(256)]
for instruction in instructions:
	label, remove, assign, focal_length_string = PATTERN.match(instruction).groups()
	box = boxes[hash(label)]
	if remove is not None:
		try:
			box.remove(label)
		except ValueError:
			pass
	else:
		try:
			index = box.index(label)
			box[index] = label
		except ValueError:
			box.append(label)
		focal_lengths[label] = int(focal_length_string)

print(sum((1 + bi) * (1 + si) * focal_lengths[label] for bi, box in enumerate(boxes) for si, label in enumerate(box)))
