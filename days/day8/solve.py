#!/usr/bin/env python

import itertools

with open("input") as f:
    data = [[int(c) for c in line] for line in f.read().splitlines()]

def row_visible(line):
    m = -1
    for x in line:
        if x > m:
            m = x
            yield True
            if x == 9:
                break
        else:
            yield False


def scenic_score(data, x, y):
    n = len(data)
    t = data[y][x]

    right = 0
    for i in range(x + 1, n):
        right += 1
        if data[y][i] >=t:
            break

    left = 0
    for i in reversed(range(0, x)):
        left += 1
        if data[y][i] >= t:
            break

    down = 0
    for i in range(y + 1, n):
        down += 1
        if data[i][x] >= t:
            break

    up = 0
    for i in reversed(range(0, y)):
        up += 1
        if data[i][x] >= t:
            break

    return up * down * left * right


n = len(data)
vis = [[False] * n for _ in range(n)]
for i in range(n):
    for x, v in enumerate(row_visible(data[i])):
        vis[i][x] |= v

    for x, v in enumerate(row_visible(reversed(data[i]))):
        vis[i][n - x - 1] |= v

    for y, v in enumerate(row_visible((data[j][i] for j in range(n)))):
        vis[y][i] |= v

    for y, v in enumerate(row_visible((data[j][i] for j in reversed(range(n))))):
        vis[n - y - 1][i] |= v

part1 = sum(itertools.chain.from_iterable(vis))
print(f"{part1 = }")

part2 = max(scenic_score(data, x, y) for x, y in itertools.product(range(n), repeat=2))
print(f"{part2 = }")
