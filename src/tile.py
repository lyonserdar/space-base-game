"""
tile.py
"""
from enum import Enum
from typing import Callable


class Tile:
    """
    Tile class
    """

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    @property
    def position(self) -> tuple:
        return (self.x, self.y)

    @position.setter
    def position(self, value: tuple) -> None:
        self.x, self.y = value

    def is_neighbor(self, tile: "Tile", check_diagonal: bool = False) -> bool:
        if abs(self.x - tile.x) + abs(self.y - tile.y) == 1:
            return True

        if check_diagonal:
            if abs(self.x - tile.x) == 1 and abs(self.y - tile.y) == 1:
                return True

        return False
