"""
Background Manager
"""
import pyglet
from pyglet.window import key, mouse
import math

from . import constants
from . import resources
from .camera import Camera
from .input_manager import InputManager
from .camera_manager import CameraManager
from .world_manager import WorldManager
from .sound_manager import SoundManager
from .sprite_manager import SpriteManager
from .tile import Tile
from .structure import Structure
from .job import Job
from .manager import Manager


class BackgroundManager(Manager):
    """
    Background Manager
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init(self) -> None:
        self.batch = pyglet.graphics.Batch()

        self.sprite = pyglet.sprite.Sprite(resources.background, batch=self.batch)

    def set_tile_info(self, text: str) -> None:
        self.tile_label.text = text

    def update(self, dt) -> None:
        pass
