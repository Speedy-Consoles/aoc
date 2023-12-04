import sys
import math
import collections

recipes = {}
for l in sys.stdin:
	educts_string, product_string = l.split(' => ')
	educt_strings = educts_string.split(', ')
	educts = {}
	for educt_string in educt_strings:
		amount_string, name = educt_string.split()
		educts[name] = int(amount_string)
	product_amount_string, product_name = product_string.split()
	recipes[product_name] = (int(product_amount_string), educts)

shopping_list = collections.defaultdict(lambda: 0, FUEL=1)

needed = 'FUEL'
try:
	while True:
		recipe = recipes[needed]
		product_amount = recipe[0]
		educts = recipe[1]
		recipe_factor = math.ceil(shopping_list[needed] / product_amount)
		shopping_list[needed] -= product_amount * recipe_factor
		for name, amount in educts.items():
			shopping_list[name] += amount * recipe_factor
		needed = next(n for n, a in shopping_list.items() if a > 0 and n != 'ORE')
except StopIteration:
	pass

print(shopping_list['ORE'])
