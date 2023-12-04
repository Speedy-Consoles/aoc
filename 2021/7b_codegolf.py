a=[int(c)for c in input().split(',')]
b=sum(a)//len(a)
print(sum(((x-b)**2+abs(x-b))//2 for x in a))
