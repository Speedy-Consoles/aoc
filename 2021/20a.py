import sys


def enhance(image, background, lut):
	width = len(image[0])
	height = len(image)
	new_width = width + 2
	new_height = height + 2
	enhanced_image = []
	for y in range(new_height):
		line = ''
		for x in range(new_width):
			index = 0
			shift = 8
			for yo in range(3):
				ny = y + yo - 2
				for xo in range(3):
					nx = x + xo - 2
					if nx < 0 or nx >= width or ny < 0 or ny >= height:
						value = background
					else:
						value = image[ny][nx]
					index += int(value == '#') << shift
					shift -= 1
			line += lut[index]
		enhanced_image.append(line)

	return lut[int(background == '#')], enhanced_image


lut, image_string = sys.stdin.read().split('\n\n')
image = image_string.splitlines()
background = '.'

for i in range(2):
	background, image = enhance(image, background, lut)

print(sum(1 for line in image for x in line if x == '#'))
