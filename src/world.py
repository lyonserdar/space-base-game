"""
Word class for world data
"""
from collections import deque
from typing import Callable

from .tile import Tile
from .structure import Structure
from .job import Job


class World:
    """
    World class
    """

    def __init__(
        self,
        width: int = 100,
        height: int = 100,
    ):
        self.width: int = width
        self.height: int = height

        self.tiles: dict[(int, int), Tile] = {}
        self.structures: dict[(int, int), Structure] = {}
        self.blueprints: dict[str, Structure] = {}
        self._on_tile_changed_callbacks = set()
        self._on_structure_changed_callbacks = set()

        # TODO: refactor to job manager
        self.jobs = deque()

        self.initialize_tiles()

        self.blueprints = {
            "wall": Structure.create_blueprint(
                type_="wall",
                movement_speed=0.0,
            )
        }

    # Subscriptions
    def subscribe_on_tile_changed(self, fn):
        self._on_tile_changed_callbacks.add(fn)

    def unsubscribe_on_tile_changed(self, fn):
        self._on_tile_changed_callbacks.remove(fn)

    def subscribe_on_structure_changed(self, fn):
        self._on_structure_changed_callbacks.add(fn)

    def unsubscribe_on_structure_changed(self, fn):
        self._on_structure_changed_callbacks.remove(fn)

    def on_tile_changed(self, tile: Tile) -> None:
        for callback in self._on_tile_changed_callbacks:
            callback(tile)

    def on_structure_changed(self, structure: Structure) -> None:
        for callback in self._on_structure_changed_callbacks:
            callback(structure)

    def initialize_tiles(self):
        """Initializes the tiles dictionary with empty tiles"""
        for x in range(self.width):
            for y in range(self.height):
                tile = Tile(x, y)
                tile.subscribe_on_tile_changed(self.on_tile_changed)
                self.tiles[(x, y)] = tile

        print(f"World created with {self.width}x{self.height} tiles")

    def get_tile_at(self, x: int, y: int) -> Tile | None:
        """Returns the Tile object at given coordinates"""
        if (x, y) not in self.tiles:
            return None
        return self.tiles[(x, y)]

    def is_structure_valid_position(self, type_: str, tile: Tile) -> bool:
        return self.blueprints[type_].is_valid_position(tile)

    def get_structure_neighbors(self, structure: Structure) -> list[Structure]:
        neighbors = []

        x = structure.tile.x
        y = structure.tile.y

        w = (x - 1, y + 0)
        n = (x + 0, y + 1)
        e = (x + 1, y + 0)
        s = (x + 0, y - 1)
        nw = (x - 1, y + 1)
        ne = (x + 1, y + 1)
        se = (x + 1, y - 1)
        sw = (x - 1, y - 1)

        if w in self.structures:
            neighbors.append(self.structures[w])
        if n in self.structures:
            neighbors.append(self.structures[n])
        if e in self.structures:
            neighbors.append(self.structures[e])
        if s in self.structures:
            neighbors.append(self.structures[s])
        if nw in self.structures:
            neighbors.append(self.structures[nw])
        if ne in self.structures:
            neighbors.append(self.structures[ne])
        if se in self.structures:
            neighbors.append(self.structures[se])
        if sw in self.structures:
            neighbors.append(self.structures[sw])

        return neighbors

    def place_structure(self, type_: str, tile: Tile) -> None:
        if type_ not in self.blueprints:
            return

        if (tile.x, tile.y) in self.structures:
            return

        structure = Structure.build_blueprint(self.blueprints[type_], tile)
        structure.subscribe_on_structure_changed(self.on_structure_changed)

        if structure:
            self.structures[(tile.x, tile.y)] = structure

            neighbors = self.get_structure_neighbors(structure)
            for neighbor in neighbors:
                self.on_structure_changed(neighbor)

            self.on_structure_changed(structure)
