def format_ground(ground):
	return ''.join('_' if g else '.' for g in ground)

def can_pass(ground):
	with_walk, with_jump = pass_ways(ground)
	return with_walk or with_jump

def pass_ways(ground):
	with_walk = len(ground) == 0 or (ground[0] and can_pass(ground[1:]))
	with_jump = len(ground) <= 3 or (ground[3] and can_pass(ground[4:]))
	return with_walk, with_jump

ground_length = 9
extended_ground_length = 5
min_terms = []
dont_care_terms = []
ground = [True] * (ground_length + extended_ground_length)
for i in range(2**ground_length):
	for d in range(ground_length):
		ground[d] = (i >> d) % 2 == 1

	outcome_examples = {}
	if not can_pass(ground[:ground_length]):
		result = 'x'
		dont_care_terms.append(i)
	else:
		walk_safe = True
		jump_safe = True
		for j in range(2**extended_ground_length):
			for d in range(extended_ground_length):
				ground[ground_length + d] = (j >> d) % 2 == 1

			with_walk, with_jump = pass_ways(ground)

			if not (with_walk or with_jump):
				continue

			outcome_examples[(with_walk, with_jump)] = format_ground(ground)
			if not with_walk:
				walk_safe = False
			if not with_jump:
				jump_safe = False

		if walk_safe == jump_safe:
			result = 'x'
			dont_care_terms.append(i)
		elif walk_safe:
			result = '0'
		else:
			result = '1'
			min_terms.append(i)

	print('{:>3}: {} o{}'.format(i, result, format_ground(ground[:ground_length])))
	if len(outcome_examples) > 1:
		for with_walk, with_jump in outcome_examples:
			if with_walk and with_jump:
				result = 'x'
			elif with_walk:
				result = '0'
			else:
				result = '1'
			print('     {} o{}'.format(result, outcome_examples[(with_walk, with_jump)]))
		

print('min terms:')
print(','.join(str(x) for x in min_terms))
print('')
print('dont care terms:')
print(','.join(str(x) for x in dont_care_terms))
