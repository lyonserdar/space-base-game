"""
World Controller
"""
import pyglet
from pyglet.sprite import Sprite
import random

from . import constants
from . import resources
from .world import World
from .tile import TileType, Tile


class WorldController:
    """
    World Controller
    """

    def __init__(
        self,
        batch: pyglet.graphics.Batch,
        group: pyglet.graphics.OrderedGroup,
    ):
        self.batch = batch
        self.group = group

        self.world = World()

        self.sprites: dict[(x, y), pygame.sprite.Sprite] = {}
        self.create_sprites()
        self.randomize_tiles()

        # pyglet.clock.schedule_interval(self.randomize_tiles, 2)

    def create_sprites(self) -> None:
        """Creates the sprites and initializes the sprites dictionary"""
        for x in range(self.world.width):
            for y in range(self.world.height):
                tile: Tile = self.world.tiles[(x, y)]
                # Register the callback
                tile.on_type_change = self.on_type_change

                if tile.type is not TileType.EMPTY:
                    sprite = Sprite(
                        resources.tiles[tile.type],
                        x * constants.TILE_SIZE,
                        y * constants.TILE_SIZE,
                        batch=self.batch,
                        group=self.group,
                    )
                    self.sprites[(x, y)] = sprite
                else:
                    self.sprites[(x, y)] = None

        print("Sprites created")

    def randomize_tiles(self, dt=None) -> None:
        """Debug tool that randomizes the tiles"""
        for x in range(self.world.width):
            for y in range(self.world.height):
                tile = self.world.tiles[(x, y)]
                if random.randint(0, 1):
                    tile.type = TileType.EMPTY
                else:
                    tile.type = TileType.FLOOR

    def on_type_change(self, tile: Tile) -> None:
        """This is a callback function that tile calles when its type changes"""
        x = tile.x
        y = tile.y

        if (x, y) in self.sprites:
            if tile.type is TileType.EMPTY:
                self.sprites[(x, y)] = None
            else:
                sprite = Sprite(
                    resources.tiles[tile.type],
                    x * constants.TILE_SIZE,
                    y * constants.TILE_SIZE,
                    batch=self.batch,
                    group=self.group,
                )
                self.sprites[(x, y)] = sprite
