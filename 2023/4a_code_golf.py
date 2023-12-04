import sys;print(sum(int(2**(len(set.intersection(*map(lambda x:set(map(int,x.split())),line[:-1].split(':')[1].split('|'))))-1)//1)for line in sys.stdin.readlines()))
