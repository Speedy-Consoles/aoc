import sys
import re

pattern = re.compile('^([a-z]+(?: [a-z]+)*) \\(contains ([a-z]+(?:, [a-z]+)*)\\)$')

allergens = set()
unused_info = []
for line in sys.stdin.read().splitlines():
	match = pattern.search(line)
	if match is None:
		print('ALARM!')
		sys.exit(1)
	ingred = match.group(1).split()
	aller = match.group(2).split(', ')
	allergens.update(aller)
	unused_info.append((ingred, aller))

allergen_by_food = {}
remaining_allergens = allergens.copy()
while len(remaining_allergens) > 0:
	for allergen in remaining_allergens.copy():
		possible_foods = set.intersection(*(set(f) for f, a in unused_info if allergen in a))
		if len(possible_foods) == 1:
			food = next(iter(possible_foods))
			allergen_by_food[food] = allergen
			for f, a in unused_info:
				if food in f:
					f.remove(food)
					if allergen in a:
						a.remove(allergen)
			remaining_allergens.remove(allergen)

answer = ','.join(f for f, a in sorted(allergen_by_food.items(), key=lambda x: x[1]))

print(answer)
