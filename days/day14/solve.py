#!/usr/bin/env python

import numpy as np

EMPTY = 0
SOLID = 1
SAND = 2
SETTLED_SAND = 3

with open("input") as f:
    data = [[tuple(map(int, pair.split(","))) for pair in line.split(" -> ")] for line in f.read().splitlines()]

grid = np.zeros((1000, 1000), dtype="uint")

for line in data:
    for (start_x, start_y), (end_x, end_y) in zip(line, line[1:]):
        if start_x > end_x:
            end_x, start_x = start_x, end_x

        if start_y > end_y:
            end_y, start_y = start_y, end_y

        grid[start_y:end_y+1,start_x:end_x+1] = 1

def sim_one_grain(grid, max_y):
    x, y = 500, 0

    while True:
        if y == max_y:
            return True

        if grid[y+1,x] == EMPTY:
            x, y = x, y + 1
        elif grid[y+1,x-1] == EMPTY:
            x, y = x - 1, y + 1
        elif grid[y+1,x+1] == EMPTY:
            x, y = x + 1, y + 1
        else:
            grid[y,x] = SETTLED_SAND
            return False

def sim_with_floor(grid, max_y):
    x, y = 500, 0

    while True:
        # hit the floor
        if y + 1 == max_y + 2:
            grid[y,x] = SETTLED_SAND
            break

        if grid[y+1,x] == EMPTY:
            x, y = x, y + 1
        elif grid[y+1,x-1] == EMPTY:
            x, y = x - 1, y + 1
        elif grid[y+1,x+1] == EMPTY:
            x, y = x + 1, y + 1
        else:
            grid[y,x] = SETTLED_SAND
            break

grid_save = np.copy(grid)
max_y = np.max(np.where(grid == 1)[0])
while True:
    hit_max_y = sim_one_grain(grid, max_y)
    if hit_max_y:
        break

print(f"part 1: {np.sum(grid == SETTLED_SAND)}")

while True:
    sim_with_floor(grid_save, max_y)
    if grid_save[0,500] == SETTLED_SAND:
        break

print(f"part 2: {np.sum(grid_save == SETTLED_SAND)}")
