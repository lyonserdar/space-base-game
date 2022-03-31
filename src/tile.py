"""
Tile class that stores the data about the tile and not the tile graphics
"""
from enum import Enum
from typing import Callable


class TileType(Enum):
    """
    Tile Types as enum
    """

    EMPTY = 0
    FLOOR = 1


class Tile:
    """
    Tile class
    """

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y
        self._type: TileType = TileType.EMPTY

        self._on_tile_changed_callbacks = set()

    # Subscriptions
    def subscribe_on_tile_changed(self, fn):
        self._on_tile_changed_callbacks.add(fn)

    def unsubscribe_on_tile_changed(self, fn):
        self._on_tile_changed_callbacks.remove(fn)

    @property
    def type(self) -> TileType:
        return self._type

    @type.setter
    def type(self, value: TileType) -> None:
        self._type = value

        for callback in self._on_tile_changed_callbacks:
            callback(self)
