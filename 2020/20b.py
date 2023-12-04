import math
import sys
from collections import defaultdict

MONSTER = [
	'                  # ',
	'#    ##    ##    ###',
	' #  #  #  #  #  #   ',
]

DIRS = [
	( 1,  0),
	( 0,  1),
	(-1,  0),
	( 0, -1)
]

ROTATIONS = [
	(( 1,  0), ( 0,  1)),
	(( 0, -1), ( 1,  0)),
	((-1,  0), ( 0, -1)),
	(( 0,  1), (-1,  0))
]

def rotate(image, index):
	width = len(image[0])
	height = len(image)
	rotation = ROTATIONS[index % 4]
	new_image = []
	for y in range(height):
		y -= (height - 1) / 2
		line = []
		for x in range(width):
			x -= (width - 1) / 2
			ox = int(rotation[0][0] * x + rotation[0][1] * y + (width - 1) / 2)
			oy = int(rotation[1][0] * x + rotation[1][1] * y + (height - 1) / 2)
			line.append(image[oy][ox])
		new_image.append(''.join(line))

	return new_image

def flip_vertically(image):
	return list(reversed(image))

def cut_border(image):
	return [line[1:-1] for line in image[1:-1]]

def transform(image, old_edge, new_edge, flip):
	image = rotate(image, -old_edge)
	if flip:
		image = flip_vertically(image)
	return rotate(image, new_edge)

def transform_and_cut(image, old_edge, new_edge, flipped):
	image = transform(image, old_edge, new_edge, flipped)
	return cut_border(image)

def get_image_borders(image):
	width = len(image[0])
	height = len(image)

	top = image[0]
	bottom = image[height - 1][::-1]
	left = ''.join(line[0] for line in image)[::-1]
	right = ''.join(line[width - 1] for line in image)

	assert(right != right[::-1])
	assert(top != top[::-1])
	assert(left != left[::-1])
	assert(bottom != bottom[::-1])

	return right, top, left, bottom

def read_tiles():
	tile_strings = sys.stdin.read().strip().split('\n\n')

	tiles = {}
	tiles_by_border = defaultdict(lambda: [])
	for tile_string in tile_strings:
		id_string, image_string = tile_string.split(':\n')
		tile_id = int(id_string.split()[1])
		image = image_string.splitlines()
		tiles[tile_id] = image

		for i, border in enumerate(get_image_borders(image)):
			tiles_by_border[border].append((tile_id, i))
	return tiles, tiles_by_border

def solve_puzzle(tiles, tiles_by_border):
	start_id = next(iter(tiles))
	start_tile = tiles[start_id]
	board = {(0, 0): start_tile}
	for border in get_image_borders(start_tile):
		tiles_by_border[border] = [x for x in tiles_by_border[border] if x[0] != start_id]
	fringe = [(0, 0)]

	while len(fringe) > 0:
		position = fringe.pop()
		image = board[position]
		borders = get_image_borders(image)
		for i, offset in enumerate(DIRS):
			border = borders[i]
			neighbor_position = (position[0] + offset[0], position[1] + offset[1])
			if neighbor_position not in board:
				for other_border, flip in ((border, True), (border[::-1], False)):
					if len(tiles_by_border[other_border]) > 0:
						assert(len(tiles_by_border[other_border]) == 1)
						border_tile_id, side = tiles_by_border[other_border][0]
						fringe.append(neighbor_position)
						neighbor_image = tiles[border_tile_id]
						board[neighbor_position] = transform(neighbor_image, side, (i + 2) % 4, flip)
						for b in get_image_borders(neighbor_image):
							tiles_by_border[b] = [x for x in tiles_by_border[b] if x[0] != border_tile_id]

	tile_width = len(start_tile[0]) - 2
	tile_height = len(start_tile) - 2

	grid_x_start = min(x for x, y in board)
	grid_x_end = max(x for x, y in board) + 1
	grid_y_start = min(y for x, y in board)
	grid_y_end = max(y for x, y in board) + 1

	grid_width = grid_x_end - grid_x_start
	grid_height = grid_y_end - grid_y_start

	width = tile_width * grid_width
	height = tile_height * grid_height

	image = [[None for x in range(grid_width)] for y in range(height)]

	for i, ty in enumerate(range(grid_y_start, grid_y_end)):
		for j, tx in enumerate(range(grid_x_start, grid_x_end)):
			for y, line in enumerate(reversed(cut_border(board[(tx, ty)]))):
				image[i * tile_height + y][j] = line

	for y in range(height):
		image[y] = ''.join(image[y])

	return image

def count_white_pixels(image):
	return sum(1 for line in image for x in line if x == '#')

def count_monsters(image):
	width = len(image[0])
	height = len(image)
	monster_width = len(MONSTER[0])
	monster_height = len(MONSTER)
	num_monsters = 0
	for start_y in range(height - monster_height):
		for start_x in range(width - monster_width):
			fail = False
			for my in range(monster_height):
				for mx in range(monster_width):
					mp = MONSTER[my][mx]
					if mp == '#':
						x = start_x + mx
						y = start_y + my
						ip = image[y][x]
						if ip != '#':
							fail = True
							break
				if fail:
					break
			if not fail:
				num_monsters += 1

	return num_monsters

tiles, tiles_by_border = read_tiles()
image = solve_puzzle(tiles, tiles_by_border)

num_monsters = 0
for i in range(2):
	for j in range(4):
		num_monsters += count_monsters(image)
		image = rotate(image, 1)
	image = flip_vertically(image)

print(count_white_pixels(image) - num_monsters * count_white_pixels(MONSTER))
