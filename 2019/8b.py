import collections

data = [x for x in input()]

width = 25
height = 6
size = width * height
num_layers = len(data) // size

layers = [data[size * i:size * (i + 1)] for i in range(num_layers)]

palette = {'0': ' ', '1': '█'}
image = ['X'] * size
for i in range(size):
	if image[i] != 'X':
		continue
	for layer in layers:
		if layer[i] != '2':
			image[i] = palette[layer[i]]
			break

for r in range(height):
	print(''.join(image[width * r:width * (r + 1)]))
