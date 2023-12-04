import collections

width = 25
height = 6
size = width * height

data = input()

num_layers = len(data) // size

layers = [data[size * i:size * (i + 1)] for i in range(num_layers)]
counters = [collections.Counter(layer) for layer in layers]
print(counters)
wanted_layer = min(counters, key=lambda c: c['0'])
print(wanted_layer['1'] * wanted_layer['2'])
