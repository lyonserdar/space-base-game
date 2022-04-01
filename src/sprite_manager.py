"""
Sprite Manager
"""
import pyglet
from pyglet.sprite import Sprite

from . import constants
from . import resources
from .world import World
from .tile import Tile
from .structure import Structure
from .world_manager import WorldManager


class SpriteManager:
    """
    Sprite Manager
    """

    def __init__(self, world_manager: WorldManager):
        self.world_manager: WorldManager = world_manager

        self.batch = pyglet.graphics.Batch()
        self.background_group = pyglet.graphics.OrderedGroup(0)
        self.forground_group = pyglet.graphics.OrderedGroup(1)
        self.gui_group = pyglet.graphics.OrderedGroup(2)

        self.structure_sprites: dict[Structure, pygame.sprite.Sprite] = {}

        self.world = self.world_manager.world
        self.world.subscribe_on_structure_changed(self.on_structure_changed)

        self.create_sprites()

    def create_sprites(self) -> None:
        # TODO: create dynamic ordering system aka groups
        for structure in self.world.structures.values():
            if structure:
                sprite = Sprite(
                    self.get_image_for_structure(structure),
                    x * constants.TILE_SIZE,
                    y * constants.TILE_SIZE,
                    batch=self.batch,
                    group=self.background_group,
                )
                self.structure_sprites[structure] = sprite

    def get_image_for_structure(self, structure: Structure):
        if structure.connected_texture:
            x = structure.tile.x
            y = structure.tile.y
            index = 0

            # TODO: fix the names?
            w = (x - 1, y + 0)
            n = (x + 0, y + 1)
            e = (x + 1, y + 0)
            s = (x + 0, y - 1)
            nw = (x - 1, y + 1)
            ne = (x + 1, y + 1)
            se = (x + 1, y - 1)
            sw = (x - 1, y - 1)

            # Check neighbors
            if w in self.world.structures:
                if self.world.structures[w].type_ == structure.type_:
                    index += 1
            if n in self.world.structures:
                if self.world.structures[n].type_ == structure.type_:
                    index += 2
            if e in self.world.structures:
                if self.world.structures[e].type_ == structure.type_:
                    index += 4
            if s in self.world.structures:
                if self.world.structures[s].type_ == structure.type_:
                    index += 8
            if nw in self.world.structures:
                if self.world.structures[nw].type_ == structure.type_:
                    if n in self.world.structures and w in self.world.structures:
                        index += 16
            if ne in self.world.structures:
                if self.world.structures[ne].type_ == structure.type_:
                    if n in self.world.structures and e in self.world.structures:
                        index += 32
            if se in self.world.structures:
                if self.world.structures[se].type_ == structure.type_:
                    if s in self.world.structures and e in self.world.structures:
                        index += 64
            if sw in self.world.structures:
                if self.world.structures[sw].type_ == structure.type_:
                    if s in self.world.structures and w in self.world.structures:
                        index += 128

            if index in resources.structures[structure.type_]:
                image = resources.structures[structure.type_][index]
            else:
                image = resources.structures[structure.type_][0]
            return image
        else:
            return resources.structures[structure.type_]

    def on_structure_changed(self, structure: Structure) -> None:
        if structure in self.structure_sprites:
            self.structure_sprites[structure].image = self.get_image_for_structure(
                structure
            )
            return

        x = structure.tile.x
        y = structure.tile.y

        # structure.on_structure_changed = self.on_structure_changed

        if structure not in self.structure_sprites:
            sprite = Sprite(
                self.get_image_for_structure(structure),
                x * constants.TILE_SIZE,
                y * constants.TILE_SIZE,
                batch=self.batch,
                group=self.forground_group,
            )
            self.structure_sprites[structure] = sprite

    def update(self, dt) -> None:
        pass
