import sys

numbers = [int(x) for x in sys.stdin.read().splitlines()]
increases = (numbers[i + 1] > numbers[i] for i in range(len(numbers) - 1))

print(sum(increases))
