#!/usr/bin/env python

from functools import reduce
import operator as op
import copy

class Monkey:
    def __init__(self, items, operation, test, true_monkey, false_monkey):
        self.activity = 0
        self.items        = items
        self.operation    = operation
        self.test         = test
        self.true_monkey  = true_monkey
        self.false_monkey = false_monkey

    def yeet(self, monkeys):
        item = self.items.pop(0)
        worry = self.operation(item) // 3
        self.activity += 1
        if worry % self.test == 0:
            monkeys[self.true_monkey].yoink(worry)
        else:
            monkeys[self.false_monkey].yoink(worry)

    def yeet_sad(self, monkeys):
        if not hasattr(self, "reducer"):
            r = reduce(op.mul, [m.test for m in monkeys])
            for m in monkeys:
                m.reducer = r

        item = self.items.pop(0)
        worry = self.operation(item) % self.reducer
        self.activity += 1
        if worry % self.test == 0:
            monkeys[self.true_monkey].yoink(worry)
        else:
            monkeys[self.false_monkey].yoink(worry)

    def yoink(self, item):
        self.items.append(item)

    def turn(self, monkeys):
        while self.items:
            self.yeet(monkeys)

    def turn_sad(self, monkeys):
        while self.items:
            self.yeet_sad(monkeys)


def parse_monkey(s):
    lines = s.splitlines()
    items = [int(x) for x in lines[1].split(": ")[1].split(", ")]
    l, oper, r = lines[2].split(" = ")[1].split()
    oper = op.mul if oper == "*" else op.add
    operation = lambda old: oper(old if l == "old" else int(l), old if r == "old" else int(r))
    test = int(lines[3].split(" ")[-1])
    tm   = int(lines[4].split(" ")[-1])
    fm   = int(lines[5].split(" ")[-1])

    return Monkey(items, operation, test, tm, fm)


def round(monkeys):
    for monkey in monkeys:
        monkey.turn(monkeys)


def round_sad(monkeys):
    for monkey in monkeys:
        monkey.turn_sad(monkeys)


def main():
    with open("input") as f:
        monkeys = [parse_monkey(s) for s in f.read().split("\n\n")]

    monkeys_orig = copy.deepcopy(monkeys)
    for _ in range(20):
        round(monkeys)

    a, b = sorted([monkey.activity for monkey in monkeys])[-2:]
    part1 = a * b
    print(f"{part1 = }")

    monkeys = monkeys_orig
    for _ in range(10000):
        round_sad(monkeys)

    a, b = sorted([monkey.activity for monkey in monkeys])[-2:]
    part2 = a * b
    print(f"{part2 = }")

if __name__ == "__main__":
    main()
