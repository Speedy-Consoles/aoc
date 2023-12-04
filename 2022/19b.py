import sys
import re
from enum import Enum
from collections import defaultdict
from copy import deepcopy
from tqdm import tqdm

TIME = 32

class Resource(Enum):
	ORE=1,
	CLAY=2,
	OBSIDIAN=3,
	GEODE=4,

PATTERN = re.compile('^Blueprint (?P<id>\\d+): Each ore robot costs (?P<ore_cost>\\d+) ore. Each clay robot costs (?P<clay_cost>\\d+) ore. Each obsidian robot costs (?P<obsidian_ore_cost>\\d+) ore and (?P<obsidian_clay_cost>\\d+) clay. Each geode robot costs (?P<geode_ore_cost>\\d+) ore and (?P<geode_obsidian_cost>\\d+) obsidian.$')

class Blueprint(object):
	def __init__(self, line):
		match = PATTERN.match(line)
		self.id = int(match.group('id'))
		self.robot_cost = {
			Resource.ORE: defaultdict(int, {Resource.ORE: int(match.group('ore_cost'))}),
			Resource.CLAY: defaultdict(int, {Resource.ORE: int(match.group('clay_cost'))}),
			Resource.OBSIDIAN: defaultdict(int, {
				Resource.ORE: int(match.group('obsidian_ore_cost')),
				Resource.CLAY: int(match.group('obsidian_clay_cost')),
			}),
			Resource.GEODE: defaultdict(int, {
				Resource.ORE: int(match.group('geode_ore_cost')),
				Resource.OBSIDIAN: int(match.group('geode_obsidian_cost')),
			}),
		}

class Inventory(object):
	def __init__(self):
		self.num_resources = defaultdict(int)
		self.num_robots = defaultdict(int)
		self.num_robots[Resource.ORE] = 1

	def update(self, new_robot_type, blueprint):
		# build robot
		result = deepcopy(self)
		if new_robot_type is not None:
			for resource, amount in blueprint.robot_cost[new_robot_type].items():
				result.num_resources[resource] -= amount

		# collect resources
		for collectee, amount in self.num_robots.items():
			result.num_resources[collectee] += amount

		# add new robot
		if new_robot_type is not None:
			result.num_robots[new_robot_type] += 1

		return result

	def can_build(self, robot_type, blueprint):
		if robot_type is None:
			return True
		for resource, amount in blueprint.robot_cost[robot_type].items():
			if self.num_resources[resource] < amount:
				return False
		return True

	def __eq__(self, other):
		return self.num_resources == other.num_resources and self.num_robots == other.num_robots

	def __hash__(self):
		return hash((
			self.num_resources[Resource.ORE],
			self.num_resources[Resource.CLAY],
			self.num_resources[Resource.OBSIDIAN],
			self.num_resources[Resource.GEODE],
			self.num_robots[Resource.ORE],
			self.num_robots[Resource.CLAY],
			self.num_robots[Resource.OBSIDIAN],
			self.num_robots[Resource.GEODE],
		))


	def __str__(self):
		return 'o: {}, c: {}, s: {}, g: {}, or: {}, cr: {}, sr: {}, gr: {}'.format(
			self.num_resources[Resource.ORE],
			self.num_resources[Resource.CLAY],
			self.num_resources[Resource.OBSIDIAN],
			self.num_resources[Resource.GEODE],
			self.num_robots[Resource.ORE],
			self.num_robots[Resource.CLAY],
			self.num_robots[Resource.OBSIDIAN],
			self.num_robots[Resource.GEODE],
		)

def get_num_cracked(blueprint, inventory, time, cut_off, cache):
	#if time > 10:
	#	print('  ' * (TIME - time), inventory)

	num_geodes = inventory.num_resources[Resource.GEODE]

	if time == 0:
		#print('  ' * (TIME - time + 1), num_geodes)
		return num_geodes

	num_geode_robots = inventory.num_robots[Resource.GEODE]
	upper_bound = num_geodes + num_geode_robots * time + time * (time - 1) // 2
	if upper_bound <= cut_off:
		#print('  ' * (TIME - time + 1), 'cut off')
		return 0

	robot_options = [Resource.GEODE]
	for robot_type in [Resource.ORE, Resource.OBSIDIAN, Resource.CLAY]:
		max_needed = max(cost[robot_type] for cost in blueprint.robot_cost.values())
		if inventory.num_robots[robot_type] < max_needed:
			robot_options.append(robot_type)
		else:
			inventory.num_resources[robot_type] = min(inventory.num_resources[robot_type], max_needed)
	robot_options.append(None)

	if (inventory, time) in cache:
		return cache[(inventory, time)]

	best_num_cracked = cut_off
	for new_robot_type in robot_options:
		if not inventory.can_build(new_robot_type, blueprint):
			continue
		new_inventory = inventory.update(new_robot_type, blueprint)
		if new_inventory is not None:
			num_cracked = get_num_cracked(blueprint, new_inventory, time - 1, best_num_cracked, cache)
			best_num_cracked = max(best_num_cracked, num_cracked)

	cache[(inventory, time)] = best_num_cracked
	return best_num_cracked

product = 1
for line in tqdm(sys.stdin.read().splitlines()[:3]):
	blueprint = Blueprint(line)
	num_cracked = get_num_cracked(blueprint, Inventory(), TIME, -1, {})
	product *= num_cracked

print(product)
