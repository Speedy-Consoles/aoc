import sys;g=set(tuple(map(int,l.split(',')))for l in sys.stdin.read().splitlines());print(sum((x+a,y+b,z+c) not in g for x,y,z in g for a,b,c in((0,0,1),(0,0,-1),(0,1,0),(0,-1,0),(1,0,0),(-1,0,0))))
