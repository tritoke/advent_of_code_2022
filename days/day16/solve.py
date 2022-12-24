#!/usr/bin/env python

import re
from functools import cache

class Graph:
    def __init__(self, connections):
        self.node_flows = {}
        self.neighbours = {}

        self.num_with_flow = 0
        for node, flow, dests in connections:
            self.node_flows[node] = flow
            self.neighbours[node] = dests
            if flow:
                self.num_with_flow += 1

    @cache
    def max_pressure_from(self, start, time_left=None, opened_valves=None) -> int:
        # print(f"[max_pressure_from] {start=}, {time_left=}, {opened_valves=}")

        if time_left is None:
            time_left = 30

        if time_left < 0:
            return 0

        if opened_valves is None:
            opened_valves = tuple()

        # open our valve?
        flow = self.node_flows[start]
        if flow > 0 and start not in opened_valves:
            valve_contribution = flow * (time_left - 1)
            opened_valves = tuple(sorted((start, *opened_valves)))

            # early exit if all are opened
            if len(opened_valves) == self.num_with_flow:
                return valve_contribution

            max_neigh_after_open = max([self.max_pressure_from(n, time_left - 2, opened_valves) for n in self.neighbours[start]])

            return valve_contribution + max_neigh_after_open
            # return max(valve_contribution + max_neigh_after_open, max_neigh)
        else:
            max_neigh = max([self.max_pressure_from(n, time_left - 1, opened_valves) for n in self.neighbours[start]])
            return max_neigh

    @cache
    def what_the_fuck_man(self, node, elephant_node, time_left=None, opened_valves=None) -> int:
        # print(f"[what_the_fuck_man] {node=}, {time_left=}, {opened_valves=}")

        if time_left is None:
            # gotta train the elephant, smh skill issue
            time_left = 26

        if time_left < 0:
            return 0

        if opened_valves is None:
            opened_valves = tuple()

        # what if we opened our valve?
        flow = self.node_flows[node]
        elephant_flow = self.node_flows[elephant_node]
        valve_contribution = 0
        human_moves = None
        elephant_moves = None

        # first see if we can open the human's valve
        if flow > 0 and node not in opened_valves:
            opened_valves = tuple(sorted((node, *opened_valves)))
            valve_contribution += flow * (time_left - 1)
            # print(f"[what_the_fuck_man] hum_added - {opened_valves=}, {valve_contribution=}")

            if len(opened_valves) == self.num_with_flow:
                return valve_contribution

            # human now cannot move
            human_moves = [node]

        # now see if the elephant can open a valve
        if elephant_flow > 0 and elephant_node not in opened_valves:
            opened_valves = tuple(sorted((elephant_node, *opened_valves)))
            valve_contribution += elephant_flow * (time_left - 1)
            # print(f"[what_the_fuck_man] ele_added - {opened_valves=}, {valve_contribution=}")

            if len(opened_valves) == self.num_with_flow:
                return valve_contribution

            # elephant now cannot move
            elephant_moves = [elephant_node]

        if human_moves is None:
            human_moves = self.neighbours[node]

        if elephant_moves is None:
            elephant_moves = self.neighbours[elephant_node]

        max_sub = max(
            self.what_the_fuck_man(hum, ele, time_left - 1, opened_valves)
            for hum in human_moves
            for ele in elephant_moves
            if hum != ele
        )

        return valve_contribution + max_sub

def main():
    pat = re.compile(r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)")
    with open("input") as f:
        data = [pat.match(line).groups() for line in f.read().splitlines()]
        data = [(start, int(flow), dests.split(", ")) for start, flow, dests in data]

    g = Graph(data)
    print(f"part 1: {g.max_pressure_from('AA')}")
    print(f"part 2: {g.what_the_fuck_man('AA', 'AA')}")


if __name__ == "__main__":
    main()
