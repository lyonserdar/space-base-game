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

from .manager import Manager


class SpriteManager(Manager):
    """
    Sprite Manager
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init(self, world_manager: WorldManager) -> None:
        self.world_manager: WorldManager = world_manager
        self.batch = pyglet.graphics.Batch()
        self.background_group = pyglet.graphics.OrderedGroup(0)
        self.forground_group = pyglet.graphics.OrderedGroup(1)
        self.gui_group = pyglet.graphics.OrderedGroup(2)

        self.structure_sprites: dict[Structure, pygame.sprite.Sprite] = {}

        self.world_manager.world.subscribe_on_structure_changed(
            self.on_structure_changed
        )

        self.world = self.world_manager.world

        self.create_sprites()

    def create_sprites(self) -> None:
        # TODO: create dynamic ordering system aka groups
        for structure in self.world_manager.world.structures.values():
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

            world = self.world_manager.world

            w = world.get_tile_at(x - 1, y + 0)
            n = world.get_tile_at(x + 0, y + 1)
            e = world.get_tile_at(x + 1, y + 0)
            s = world.get_tile_at(x + 0, y - 1)
            nw = world.get_tile_at(x - 1, y + 1)
            ne = world.get_tile_at(x + 1, y + 1)
            se = world.get_tile_at(x + 1, y - 1)
            sw = world.get_tile_at(x - 1, y - 1)

            # Check neighbors
            if w in world.structures:
                if structure.type_ in (s.type_ for s in world.structures[w]):
                    index += 1
            if n in world.structures:
                if structure.type_ in (s.type_ for s in world.structures[n]):
                    index += 2
            if e in world.structures:
                if structure.type_ in (s.type_ for s in world.structures[e]):
                    index += 4
            if s in world.structures:
                if structure.type_ in (s.type_ for s in world.structures[s]):
                    index += 8
            if nw in world.structures:
                if (
                    structure.type_ in (s.type_ for s in world.structures[nw])
                    and structure.type_ in (s.type_ for s in world.structures[n])
                    and structure.type_ in (s.type_ for s in world.structures[w])
                ):
                    index += 16
            if ne in world.structures:
                if (
                    structure.type_ in (s.type_ for s in world.structures[ne])
                    and structure.type_ in (s.type_ for s in world.structures[n])
                    and structure.type_ in (s.type_ for s in world.structures[e])
                ):
                    index += 32
            if se in world.structures:
                if (
                    structure.type_ in (s.type_ for s in world.structures[se])
                    and structure.type_ in (s.type_ for s in world.structures[s])
                    and structure.type_ in (s.type_ for s in world.structures[e])
                ):
                    index += 64
            if sw in world.structures:
                if (
                    structure.type_ in (s.type_ for s in world.structures[sw])
                    and structure.type_ in (s.type_ for s in world.structures[s])
                    and structure.type_ in (s.type_ for s in world.structures[w])
                ):
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
