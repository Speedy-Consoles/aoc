x=0
for s in input().split(','):
	h=0
	for c in s:
		h=(h+ord(c))*17%256
	x+=h
print(x)
