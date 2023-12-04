import sys
from collections import defaultdict

def get_image_borders(image):
	width = len(image[0])
	height = len(image)

	top = min(int(image[0]), int(image[0][::-1]))
	bottom = min(int(image[height - 1]), int(image[height - 1][::-1]))

	left_string = ''.join(line[0] for line in image)
	left = min(int(left_string), int(left_string[::-1]))

	right_string = ''.join(line[width - 1] for line in image)
	right = min(int(right_string), int(right_string[::-1]))

	return right, top, left, bottom

tile_strings = sys.stdin.read().strip().split('\n\n')

num_borders = defaultdict(lambda: 0)
tiles = {}
for tile_string in tile_strings:
	id_string, image_string = tile_string.split(':\n')
	tile_id = int(id_string.split()[1])
	image = [''.join('0' if c == '.' else '1' for c in line) for line in image_string.split('\n')]
	tiles[tile_id] = image

	for border in get_image_borders(image):
		num_borders[border] += 1

corner_product = 1
for tile_id, image in tiles.items():
	unmatched = 0
	for border in get_image_borders(image):
		if num_borders[border] != 2:
			unmatched += 1
	if unmatched == 2:
		corner_product *= tile_id

print(corner_product)
