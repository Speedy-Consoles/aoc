from functools import reduce;print(sum((reduce(lambda h,c:(h+ord(c))*17%256,s,0)for s in input().split(','))))
