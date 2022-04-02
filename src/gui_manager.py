"""
GUI Manager
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


class GUIManager(Manager):
    """
    GUI Manager
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init(self, window: pyglet.window.Window, input_manager: InputManager) -> None:
        self.window: pyglet.window.Window = window
        self.input_manager: InputManager = input_manager
        self.fps_display = pyglet.window.FPSDisplay(self.window)
        self.batch = pyglet.graphics.Batch()
        self.tile_label = pyglet.text.Label("(0, 0)", x=10, y=50, batch=self.batch)

    def set_tile_info(self, text: str) -> None:
        self.tile_label.text = text

    def update(self, dt) -> None:
        pass
