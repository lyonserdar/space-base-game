"""
Word class for world data
"""
from .tile import Tile


class World:
    """
    World class
    """

    def __init__(self, width: int = 100, height: int = 100):
        self.width = width
        self.height = height

        self.tiles: dic[(int, int), Tile] = {}
        self.initialize_tiles()

    def initialize_tiles(self):
        """Initializes the tiles dictionary with empty tiles"""
        for x in range(self.width):
            for y in range(self.height):
                tile = Tile(x, y)
                self.tiles[(x, y)] = tile

        print(f"World created with {self.width}x{self.height} tiles")

    def get_tile_at(self, x: int, y: int) -> Tile | None:
        """Returns the Tile object at given coordinates"""
        if (x, y) not in self.tiles:
            return None
        return self.tiles[(x, y)]
