import sys

numbers = [int(x) for x in sys.stdin.read().splitlines()]
increases = (numbers[i + 3] > numbers[i] for i in range(len(numbers) - 3))

print(sum(increases))
