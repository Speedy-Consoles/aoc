public_keys = (int(input()), int(input()))

def brute_force(subject_number, public_key):
	counter = 0
	value = 1
	while value != public_key:
		value = (value * subject_number) % 20201227
		counter += 1
	return counter

def transform(subject_number, loop_size):
	value = 1
	for i in range(loop_size):
		value = (value * subject_number) % 20201227
	return value

loop_size1 = brute_force(7, public_keys[0])

encryption_key = transform(public_keys[1], loop_size1)
print(encryption_key)
