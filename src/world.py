"""
Word class for world data
"""
from typing import Callable
from .tile import Tile
from .structure import Structure


class World:
    """
    World class
    """

    def __init__(
        self,
        width: int = 100,
        height: int = 100,
        tiles: dict[(int, int), Tile] = {},
        structures: dict[(int, int), Structure] = {},
        blueprints: dict[str, Structure] = {},
        on_structure_created: Callable[[], Structure] = None,
    ):
        self.width = width
        self.height = height
        self.tiles = tiles
        self.structures = structures
        self.blueprints = blueprints
        self.on_structure_created = on_structure_created

        self.initialize_tiles()

        self.blueprints = {
            "wall": Structure.create_blueprint(
                type_="wall",
                movement_speed=0.0,
                width=1,
                height=1,
            )
        }

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

    def place_structure(self, type_: str, tile: Tile) -> None:
        if type_ not in self.blueprints:
            return

        if (tile.x, tile.y) in self.structures:
            return

        structure = Structure.build_blueprint(self.blueprints[type_], tile)
        self.structures[(tile.x, tile.y)] = structure

        # Let the world controller know
        if self.on_structure_created:
            self.on_structure_created(structure)
