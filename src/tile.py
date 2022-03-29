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
        self._type: TileType = TileType.EMPTY
        self.on_type_change: Callable[[], Tile] = None
        self.x: int = x
        self.y: int = y

    @property
    def type(self) -> TileType:
        return self._type

    @type.setter
    def type(self, value: TileType) -> None:
        self._type = value

        if self.on_type_change:
            self.on_type_change(self)
