"""
Tile class 
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
