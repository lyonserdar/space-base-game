"""
Sound Manager
"""
import pyglet

from . import resources
from .world_manager import WorldManager
from .input_manager import InputManager
from .manager import Manager


class SoundManager(Manager):
    """
    Sound Manager
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init(self, world_manager: WorldManager) -> None:
        self.world_manager: WorldManager = world_manager

        self.world_manager.world.subscribe_on_structure_changed(
            self.on_structure_changed
        )

        self.structure_player = pyglet.media.Player()

    def on_structure_changed(self, structure) -> None:
        self.structure_player.queue(resources.audio["tile_changed"])
        self.structure_player.next_source()
        self.structure_player.play()

    def update(self, dt) -> None:
        pass
