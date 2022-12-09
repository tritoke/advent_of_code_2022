#!/usr/bin/env python

import string
from functools import reduce
import operator as op

with open("input") as f:
    data = list(f.read().splitlines())

comp = [(d[:len(d)//2], d[len(d)//2:]) for d in data]

def prio(c):
    return string.ascii_letters.index(c) + 1

part1 = 0
for a, b in comp:
    diff = next(iter(set(a) & set(b)))
    part1 += prio(diff)
print(part1)

part2 = 0
for i in range(0, len(comp), 3):
    group = comp[i:i+3]
    common = next(iter(reduce(set.intersection, (set(a).union(set(b)) for a,b in group))))
    part2 += prio(common)

print(part2)
