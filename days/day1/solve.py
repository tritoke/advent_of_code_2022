#!/usr/bin/env python

with open("input") as f:
    sums = sorted(sum(int(x) for x in s.splitlines()) for s in f.read().split("\n\n"))[::-1]

part1 = sums[0]
part2 = sum(sums[0:3])

print(part1, part2)
