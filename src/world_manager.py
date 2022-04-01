"""
World Manager
"""
import pyglet

from .world import World
from .tile import Tile
from .structure import Structure


class WorldManager:
    """
    World Manager
    """

    def __init__(self):
        self.world: World = World()
        self.world.subscribe_on_structure_changed(self.on_structure_changed)

    def on_structure_changed(self, structure: Structure) -> None:
        pass

    def update(self, dt) -> None:
        pass
