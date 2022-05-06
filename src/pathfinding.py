"""
pathfinding.py
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from .tile import Tile

if TYPE_CHECKING:
    from .world import World


T = TypeVar("T")


class Node(Generic[T]):
    """
    Node
    """

    def __init__(self, data: T):
        self.data: T = data
        self.edges: list[Edge] = []


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
                        self_cost = 1 - sum(
                            s.movement_speed for s in world.structures[tile]
                        )
                        neighbor_cost = 1 - sum(
                            s.movement_speed for s in world.structures[neighbor_tile]
                        )
                        cost = (self_cost + neighbor_cost) / 2
                        edge = Edge(cost, self.nodes[neighbor_tile])
                        node.edges.append(edge)
                        count += 1

        return count
