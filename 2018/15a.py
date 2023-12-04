import sys
import functools
from enum import Enum

@functools.total_ordering
class Vec:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __add__(self, other):
		return Vec(self.x + other.x, self.y + other.y)

	def __eq__(self, other):
		if type(self) != type(other):
			return False
		return self.x == other.x and self.y == other.y

	def __lt__(self, other):
		if type(self) != type(other):
			return NotImplemented
		return self.y < other.y or (self.y == other.y and self.y < other.y)

	def __hash__(self):
		return hash((self.x, self.y))

	def __str__(self):
		return '({}, {})'.format(self.x, self.y)

	def __repr__(self):
		return 'Vec({}, {})'.format(self.x, self.y)

class Faction(Enum):
	ELVES = 0
	GOBLINS = 1

	def enemy(self):
		if self == Faction.ELVES:
			return Faction.GOBLINS
		elif self == Faction.GOBLINS:
			return Faction.ELVES
		return None

class Unit:
	def __init__(self, faction):
		self.health = 200
		self.faction = faction

class Board:
	def __init__(self, board_string):
		self.fields = []
		self.num_units = { Faction.ELVES: 0, Faction.GOBLINS: 0 }
		for y, row in enumerate(board_string.splitlines()):
			field_row = []
			for x, character in enumerate(row):
				position = Vec(x, y)
				if character == '#':
					field = '#'
				elif character == 'E':
					field = Unit(Faction.ELVES)
					self.num_units[Faction.ELVES] += 1
				elif character == 'G':
					field = Unit(Faction.GOBLINS)
					self.num_units[Faction.GOBLINS] += 1
				else:
					field = None
				field_row.append(field)
			self.fields.append(field_row)

	def __getitem__(self, key):
		return self.fields[key.y][key.x]

	def __setitem__(self, key, value):
		self.fields[key.y][key.x] = value

	def __iter__(self):
		for y, row in enumerate(self.fields):
			for x, field in enumerate(row):
				yield Vec(x, y), field

	def move(self, position, new_position):
		unit = self[position]
		assert(type(unit) == Unit)
		self[position] = None
		assert(self[new_position] is None)
		self[new_position] = unit

	def damage(self, position):
		unit = self[position]
		assert(type(unit) == Unit)
		unit.health -= 3
		if unit.health <= 0:
			self[position] = None
			self.num_units[unit.faction] -= 1

	def total_health(self):
		return sum(field.health for row in self.fields for field in row if type(field) == Unit)

	def done(self):
		return any(x == 0 for x in self.num_units.values())

	def print(self, with_health=False, marked_fields=set()):
		for y, row in enumerate(self.fields):
			health_string = ''
			for x, field in enumerate(row):
				position = Vec(x, y)
				if position in marked_fields:
					character = 'X'
				elif type(field) == Unit:
					character = 'E' if field.faction == Faction.ELVES else 'G'
					if health_string == '':
						health_string += '   '
					else:
						health_string += ', '
					health_string += character + '({})'.format(field.health)
				elif field is None:
					character = '.'
				else:
					character = field
				print(character, end='')
			if with_health:
				print(health_string)
			else:
				print()

DIRECTIONS = [Vec(0, -1), Vec(-1, 0), Vec(1, 0), Vec(0, 1)]
VERBOSE = False

def get_neighboring_unit_position(board, position, faction):
	enemy_position = None
	for d in DIRECTIONS:
		neighbor_position = position + d
		neighbor_field = board[neighbor_position]
		if type(neighbor_field) == Unit and neighbor_field.faction == faction:
			if enemy_position is None or neighbor_field.health < board[enemy_position].health:
				enemy_position = neighbor_position
	return enemy_position

def get_move_direction(board, my_position, enemy_faction):
	fringe = []
	for d in DIRECTIONS:
		neighbor_position = my_position + d
		neighbor_field = board[neighbor_position]
		if neighbor_field is None:
			fringe.append((neighbor_position, d))
	seen = { p for p, d in fringe }
	target_position = None
	move_direction = None
	while target_position is None and len(fringe) > 0:
		new_fringe = []
		for current_position, start_direction in fringe:
			for direction in DIRECTIONS:
				next_position = current_position + direction
				next_field = board[next_position]
				if type(next_field) == Unit:
					if next_field.faction == enemy_faction:
						if target_position is None or current_position < target_position:
							target_position = current_position
							move_direction = start_direction
				elif next_field == None and next_position not in seen:
					new_fringe.append((next_position, start_direction))
					seen.add(next_position)
		fringe = new_fringe

	return move_direction

board = Board(sys.stdin.read())

if VERBOSE:
	print('Initially:')
	board.print(with_health=True)

num_completed_rounds = 0
while not board.done():
	units = [(position, field) for position, field in board if type(field) == Unit]
	full_round = True
	for my_position, my_field in units:
		if board.done():
			full_round = False
			break
		if board[my_position] is not my_field:
			continue

		enemy_faction = my_field.faction.enemy()

		# find neighboring enemy
		enemy_position = get_neighboring_unit_position(board, my_position, enemy_faction)

		# move
		if enemy_position is None:
			move_direction = get_move_direction(board, my_position, enemy_faction)
			if move_direction is not None:
				board.move(my_position, my_position + move_direction)
				my_position += move_direction
				# find neighboring enemy again
				enemy_position = get_neighboring_unit_position(board, my_position, enemy_faction)

		# fight
		if enemy_position is not None:
			board.damage(enemy_position)

	if VERBOSE:
		print()
		print('After {} round:'.format(num_completed_rounds + 1))
		board.print(with_health=True)

	if full_round:
		num_completed_rounds += 1


print(num_completed_rounds * board.total_health())
