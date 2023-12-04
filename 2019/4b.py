print(len([x for x in (str(x) for x in range(183564, 657474)) if list(x) == sorted(x) and any(x.count(str(y)) == 2 for y in range(10))]))
