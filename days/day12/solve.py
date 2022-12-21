#!/usr/bin/env python

from typing import Optional, Iterator, Tuple
import string
import collections

def dbg(x):
    print(f"[dbg] {x = }")
    return x

class TileGraphWrapper:
    def __init__(self, tiles):
        self.start_tile = None
        self.end_tile = None
        for y, row in enumerate(tiles):
            for x, c in enumerate(row):
                if c == 'S':
                    self.start_tile = (x, y)
                elif c == 'E':
                    self.end_tile = (x, y)


        if self.start_tile is None or self.end_tile is None:
            raise ValueError("Invalid tiles, no start and end")

        self.tiles = tiles
        self.height_map = {
            'S': 0,
            'E': 25,
            **{c: ord(c) - ord('a') for c in string.ascii_lowercase},
        }

    def __getitem__(self, key: (int, int), /) -> Optional[str]:
        x, y = key
        if x < 0 or y < 0:
            return None

        try:
            return self.tiles[y][x]
        except IndexError:
            return None

    def neighbours(self, tile: (int, int)) -> Iterator[Tuple[int, int]]:
        x, y = tile
        for xd, yd in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            neigh = (x + xd, y + yd)
            if self[neigh]:
                yield neigh

    def height(self, tile: (int, int)) -> Optional[int]:
        c = self[tile]
        if c is None:
            return None
        else:
            return self.height_map.get(c)


    def bfs_to_end(self) -> int:
        """
        uses BFS to find the shortest path to the end
        """

        q = collections.deque([self.start_tile])
        dist_map = {
            self.start_tile: 0,
        }

        while node := q.popleft():
            curr_dist = dist_map[node]

            # add the neighbours to the queue
            for n in self.neighbours(node):
                if n not in dist_map and self.height(n) <= self.height(node) + 1:
                    # return distance if this is the end node
                    if n == self.end_tile:
                        return curr_dist + 1

                    # otherwise add the nodes to the queue
                    dist_map[n] = curr_dist + 1
                    q.append(n)

        raise ValueError("bad graph, path to end node not found")


    def bfs_to_a(self) -> int:
        """
        uses BFS to find the shortest path to an a tile
        """

        q = collections.deque([self.end_tile])
        dist_map = {
            self.end_tile: 0,
        }
        while node := q.popleft():
            curr_dist = dist_map[node]

            # add the neighbours to the queue
            for n in self.neighbours(node):
                if n not in dist_map and self.height(node) <= self.height(n) + 1:
                    # return distance if this is the end node
                    if self.height(n) == 0 and self[n] != "S":
                        # if it is an a node return
                        return curr_dist + 1
                    else:
                        # otherwise add the nodes to the queue
                        dist_map[n] = curr_dist + 1
                        q.append(n)

        raise ValueError("bad graph, path to end node not found")


def main():
    with open("input") as f:
        graph = TileGraphWrapper(f.read().splitlines())

    part1 = graph.bfs_to_end()
    print(f"part 1: {part1}")

    part2 = graph.bfs_to_a()
    print(f"part 2: {part2}")

if __name__ == "__main__":
    main()
