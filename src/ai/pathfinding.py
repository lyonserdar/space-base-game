"""
pathfinding.py
"""
from __future__ import annotations

import heapq
from collections import defaultdict
from dataclasses import dataclass, field
from itertools import count
from math import inf
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from ..tile import Tile

if TYPE_CHECKING:
    from ..world import World


T = TypeVar("T")


class Node(Generic[T]):
    """
    Node
    """

    def __init__(self, data: T):
        self.data: T = data
        self.edges: dict["Node", Edge] = {}


class Edge:
    """
    Edge
    """

    def __init__(self, cost: float, node: Node):
        self.cost: float = cost
        self.node: Node = node


class TileGraph:
    """
    Tile Graph
    """

    def __init__(self, world: World):
        self.nodes: dict[Tile, Node] = {}
        self.world: World = world

        self.create_nodes(self.world)
        edge_count = self.create_edges(self.world)

        print(
            f"TileGraph Created with {len(self.nodes)} nodes, and {edge_count} edges!"
        )

    def create_nodes(self, world: World):
        """Creates the nodes for tiles that a structure exists and is moveable"""
        for x in range(world.width):
            for y in range(world.height):
                tile: Tile = world.get_tile_at(x, y)
                structures = world.structures[tile]

                if structures and not any(s.movement_speed == 0 for s in structures):
                    node = Node(tile)
                    self.nodes[tile] = node

    def create_edges(self, world: World) -> int:
        """Creates the edges for nodes"""
        count = 0
        for tile, node in self.nodes.items():
            for x in range(-1, 2):
                for y in range(-1, 2):
                    neighbor_tile = world.get_tile_at(tile.x + x, tile.y + y)
                    if (
                        neighbor_tile
                        and tile != neighbor_tile
                        and neighbor_tile in self.nodes
                    ):
                        neighbor_node = self.nodes[neighbor_tile]
                        self_cost = 1 - sum(
                            s.movement_speed for s in world.structures[tile]
                        )
                        neighbor_cost = 1 - sum(
                            s.movement_speed for s in world.structures[neighbor_tile]
                        )
                        cost = (self_cost + neighbor_cost) / 2
                        edge = Edge(cost, self.nodes[neighbor_tile])
                        node.edges[neighbor_node] = edge
                        count += 1

        return count


# @dataclass(order=True)
# class PrioritizedItem:
#     """Class for items used in heapq/Priority Queue"""
#     priority: int
#     item: Any=field(compare=False)


class AStar:
    """
    A Star Search Algorithm for pathfinding
    It finds a path from start to goal
    """

    def __init__(self, world: World, start: Tile, goal: Tile) -> None:
        self.world: World = world
        self.nodes: dict[Tile, Node] = world.tile_graph.nodes

        self.start: Node = None
        if start in self.nodes:
            self.start = self.nodes[start]

        self.goal: Node = None
        if goal in self.nodes:
            self.goal = self.nodes[goal]

        self.path: list[Tile] = []

        if self.goal and self.start:
            self.counter = count()
            path = self.run()
            print("Path:")
            for tile in path:
                print(tile.x, tile.y)
        else:
            print("Path:", "no path")

    def run(self) -> list[Node]:
        """Implementation of the algorithm"""
        open_set = []
        came_from: dict[Node, Node] = {}

        g_score: dict[Node, float | inf] = defaultdict(lambda: inf)
        g_score[self.start] = 0.0

        f_score: dict[Node, float | inf] = defaultdict(lambda: inf)
        f_score[self.start] = self.heuristic(self.start)

        heapq.heappush(open_set, (f_score[self.start], next(self.counter), self.start))

        while open_set:
            print("size", len(open_set))
            current = open_set[0][2]

            if current == self.goal:
                print("goal")
                return self.reconstruct_path(came_from, current)

            heapq.heappop(open_set)

            print("items", len(current.edges))
            for neighbor, edge in current.edges.items():
                tentative_g_score = g_score[current] + edge.cost

                if tentative_g_score < g_score[neighbor]:
                    print("first if")
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor)

                    if neighbor not in (n[2] for n in list(open_set)):
                        print("if")
                        heapq.heappush(
                            open_set, (f_score[neighbor], next(self.counter), neighbor)
                        )

    def reconstruct_path(
        self, came_from: dict[Node, Node], current: Node
    ) -> list[Tile]:
        """Creates the path and returns the total path as a list"""
        path = [current]

        while current in came_from:
            current = came_from[current]
            # path.insert(0, current)
            path.append(current)

        return [node.data for node in path]

    def heuristic(self, node: Node) -> float:
        """Heuristic function that uses Manhattan distance on a square grid"""
        return abs(node.data.x - self.goal.data.x) + abs(node.data.y - self.goal.data.y)
