#!/usr/bin/env python

import math

with open("input") as f:
    inp = f.read().split("\n\n")[0]
    data = [(direction, int(distance)) for direction, distance in map(str.split, inp.splitlines())]

def distance(head, tail):
    hx, hy = head
    tx, ty = tail

    return math.sqrt((hx - tx) ** 2 + (hy - ty) ** 2)

def signum(x):
    return int(math.copysign(1, x))

def bring_tail(head, tail):
    """
    update the tail based on the position of the "head"
    with the head being the next knot in front of it
    """

def move(snake, direction):
    if not hasattr(move, "dir_map"):
        move.dir_map = {
            "R": (1, 0),
            "L": (-1, 0),
            "U": (0, 1),
            "D": (0, -1),
        }

    old_head = snake[0]
    tail = snake[1:]

    dx, dy = move.dir_map[direction]
    hx, hy = old_head
    head = (hx + dx, hy + dy)

    snake = [head]
    for i, t in enumerate(tail):
        head = snake[i]
        # slightly more than sqrt(2)
        if distance(head, t) > 1.5:
            hx, hy = head
            tx, ty = t
            if hx == tx:
                diff = hy - ty
                t = (tx, ty + signum(diff) * (abs(diff) - 1))
            elif hy == ty:
                diff = hx - tx
                t = (tx + signum(diff) * (abs(diff) - 1), ty)
            else:
                xs = signum(hx - tx)
                ys = signum(hy - ty)
                t = (tx + xs, ty + ys)

        snake.append(t)

    return snake


def sim_rope(snake, instructions):
    tail_positions = {snake[-1]}
    for direc, dist in instructions:
        for _ in range(dist):
            snake = move(snake, direc)
            tail_positions.add(snake[-1])

    # print(tail_positions)
    return len(tail_positions)

p1 = sim_rope([(0, 0)] * 2, data)
print(f"part 1: {p1}")

p2 = sim_rope([(0, 0)] * 10, data)
print(f"part 2: {p2}")

