import sys
import itertools as it

try:
	from tqdm import tqdm
except:
	def tqdm(x):
		for i in x:
			print(i)
			yield i

def fft(digits, num_iterations):
	num_digits = len(digits)
	digits = digits[:]
	new_digits = [0] * num_digits
	cum_digits = [0] * (num_digits + 1)
	for i in tqdm(range(num_iterations)):
		for j, cs in enumerate(it.accumulate(digits)):
			cum_digits[j + 1] = cs
		for j in range(num_digits):
			s = 0
			for k in range(j, num_digits, 4 * (j + 1)):
				s += cum_digits[k] - cum_digits[min(num_digits, k + j + 1)]
			for k in range((j + 1) * 3 - 1, num_digits, 4 * (j + 1)):
				s -= cum_digits[k] - cum_digits[min(num_digits, k + j + 1)]
			new_digits[j] = abs(s) % 10
		tmp = digits
		digits = new_digits
		new_digits = tmp
	return digits

input_string = input() * 10000
#input_string = '03036732577212944063491565474664' * 10000
digits = [int(x) for x in input_string]
offset = int(input_string[:7])

transformed = fft(digits, 100)
print(''.join(str(d) for d in transformed)[offset:offset + 8])

