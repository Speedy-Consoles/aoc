import sys;e=lambda s:s+[s[-1]+e([b-a for a,b in zip(s,s[1:])])[-1]if any(x for x in s)else 0];print(sum(e([int(x)for x in l.split()])[-1]for l in sys.stdin.read().splitlines()))
