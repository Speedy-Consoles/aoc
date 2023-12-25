import sys
import math
import networkx as nx

def parse_line(s):
	origin, destinations_string = s.split(': ')
	return origin, destinations_string.split()

graph = nx.Graph(dict(map(parse_line, sys.stdin.read().splitlines())))

print(math.prod(map(len, nx.k_edge_components(graph, 4))))

