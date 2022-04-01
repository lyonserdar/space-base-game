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

    def __init__(
        self,
        input_manager: InputManager,
        world_manager: WorldManager,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.input_manager: InputManager = input_manager
        self.world_manager: WorldManager = world_manager
        self.cooldown: float = 0.1
        self.playing = False

        self.world_manager.world.subscribe_on_structure_changed(
            self.on_structure_changed
        )

    def on_structure_changed(self, structure) -> None:
        self.play("tile_changed")

    def reset_playing(self, dt=None):
        self.playing = False

    def play(self, audio_name: str) -> None:
        if not self.playing:
            self.playing = True
            resources.audio[audio_name].play()
            pyglet.clock.schedule_once(self.reset_playing, self.cooldown)

    def update(self, dt) -> None:
        pass
