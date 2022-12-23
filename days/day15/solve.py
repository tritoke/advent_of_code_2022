#!/usr/bin/env python

import re
from z3 import *

pat = re.compile(r"Sensor at x=(?P<SENSOR_X>-?\d+), y=(?P<SENSOR_Y>-?\d+): closest beacon is at x=(?P<BEACON_X>-?\d+), y=(?P<BEACON_Y>-?\d+)")
with open("input") as f:
    data = [tuple(map(int, pat.match(line).groups())) for line in f.read().splitlines()]


def manhattan_distance(a, b):
    ax, ay = a
    bx, by = b

    return abs(ax - bx) + abs(ay - by)

def calc_impossible_for_y(inp, y):
    groups = []

    for sx, sy, bx, by in inp:
        # calculate the manhattan distance to the beacon
        dist = manhattan_distance((sx, sy), (bx, by))

        # calculate the distance from the sensor to the given y value
        y_dist = abs(y - sy)

        # if it is too far away ignore it
        if y_dist > dist:
            continue

        # otherwise calculate the start and end point of this sensors vision into this row
        dist_either_side = dist - y_dist
        start, end = sx - dist_either_side, sx + dist_either_side

        groups.append((start, end))

    # now merge runs of groups
    # first sort them based on start position
    groups.sort()

    # now we can merge groups based 
    curr_group = None
    merged_groups = []
    for group in groups:
        # if the current group is empty check this group becomes the current one
        if curr_group is None:
            curr_group = group
            continue

        # if group starts after curr_group ends, then add curr_group to the 
        if curr_group[1] < group[0]:
            merged_groups.append(curr_group)
            current_group = group
            continue

        # if the groups overlap then update the end of the current_group with the end from group
        curr_group = (curr_group[0], max(curr_group[1], group[1]))

    # when we finish the loop append the final group
    merged_groups.append(curr_group)

    # now we can calculate the number of occupied tiles by the sum of the sizes of the merged groups
    return sum(end-start for start, end in merged_groups)

print(f"part 1: {calc_impossible_for_y(data, 2000000)}")

def locate_thingy(inp, max_v):
    # the algorithm for this is entirely different and can be encoded as a set of constraints
    s = Solver()

    x, y = Ints("x y")

    # bound constraints
    s.add(And(x >= 0, x <= max_v))
    s.add(And(y >= 0, y <= max_v))

    for sx, sy, bx, by in inp:
        # manhattan distance constraints
        dist = manhattan_distance((sx, sy), (bx, by))

        # the manhattan distance from this point to this sensor must be greater
        # than the distance from it to the beacon
        s.add((Abs(sx-x) + Abs(sy-y)) > dist)

    if s.check() == sat:
        m = s.model()
        xl = m[x].as_long()
        yl = m[y].as_long()

        return xl * 4000000 + yl
    else:
        return None

print(f"part 2: {locate_thingy(data, 4000000)}")
