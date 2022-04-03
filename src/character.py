"""
Character
"""
from .tile import Tile


class Character:
    """
    Character
    """

    def __init__(self, tile: Tile, speed: float = 10.0):
        self._x: float = 0
        self._y: float = 0
        self.speed: float = speed

        self.current_tile: Tile = tile
        self.destinaiton_tile: Tile = tile

        self.movement_percentage: float = 0.0  # Between 0.0 and 1.0

    @property
    def x(self) -> float:
        return Character.lerp(
            self.current_tile.x, self.destinaiton_tile.x, self.movement_percentage
        )

    @property
    def y(self) -> float:
        return Character.lerp(
            self.current_tile.y, self.destinaiton_tile.y, self.movement_percentage
        )

    def update(self, dt: float) -> None:
        if self.current_tile == self.destinaiton_tile:
            return

        distance_to_travel = (
            (self.current_tile.x - self.destinaiton_tile.x) ** 2
            + (self.current_tile.y - self.destinaiton_tile.y) ** 2
        ) ** (1 / 2)

        character_can_travel = self.speed * dt

        percentage_can_travel = character_can_travel / distance_to_travel

        self.movement_percentage += percentage_can_travel

        if self.movement_percentage >= 1.0:
            self.current_tile = self.destinaiton_tile
            self.movement_percentage = 0.0

    @staticmethod
    def lerp(current: float, destination: float, percentage: float) -> float:
        return (percentage * current) + ((1 - percentage) * destination)
