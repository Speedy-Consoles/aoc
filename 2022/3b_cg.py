import sys;print(sum((lambda a:ord(a)-38-a.islower()*58)((a&b&c).pop())for a,b,c in(lambda l:(map(set,l[i:i+3])for i in range(0,len(l),3)))(sys.stdin.read().splitlines())))
