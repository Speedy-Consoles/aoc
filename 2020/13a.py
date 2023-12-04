import sys

arrival = int(input())
busses = [int(x) for x in input().split(',') if x != 'x']

min_wait_time = None
best_bus = None
for bus in busses:
	wait_time = -arrival % bus
	if min_wait_time is None or wait_time < min_wait_time:
		min_wait_time = wait_time
		best_bus = bus

print(best_bus * min_wait_time)
