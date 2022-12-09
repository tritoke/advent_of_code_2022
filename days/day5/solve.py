#!/usr/bin/env python

from collections import defaultdict, namedtuple
import re
import copy

Action = namedtuple("Action", ["count", "src", "dst"])

with open("input") as f:
    init_state, moves = f.read().split("\n\n")

    # parse the states
    states = defaultdict(list)
    for line in init_state.splitlines()[:-1]:
        for i, c in enumerate(line[1::4]):
            if c != " ":
                states[i + 1].insert(0, c)

    # parse the moves
    actions = [Action(int(c), int(s), int(d)) for c,s,d in re.findall(r"move (\d+) from (\d+) to (\d+)", moves)]

# apply the moves
towers = copy.deepcopy(states)
print(towers)
for action in actions:
    for _ in range(action.count):
        towers[action.dst].append(towers[action.src].pop())

part1 = "".join([towers[i + 1][-1] for i in range(len(towers))])
print(part1)

# apply the moves
towers = states
for action in actions:
    towers[action.dst].extend(towers[action.src][-action.count:])
    towers[action.src][-action.count:] = []

part2 = "".join([towers[i + 1][-1] for i in range(len(towers))])
print(part2)
