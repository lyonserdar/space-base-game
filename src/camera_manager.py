"""
Camera Manager
"""
import pyglet
from pyglet.window import key, mouse

from . import constants
from .camera import Camera
from .manager import Manager
from .input_manager import InputManager


class CameraManager(Manager):
    """
    Camera Manager
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init(self, input_manager: InputManager, window) -> None:
        self.input_manager: InputManager = input_manager
        self.window = window

        self.background_camera = Camera(self.window)
        self.camera = Camera(
            self.window,
            speed=2.0,
            # zoom_speed=1.1,
            min_zoom=1.0,
            max_zoom=8.0,
            center=True,
        )
        self.gui_camera = Camera(self.window)
        # Initialize camera position to middle of the world
        self.camera.position = (
            constants.WOLRD_WIDTH * constants.TILE_SIZE // 2,
            constants.WORLD_HEIGHT * constants.TILE_SIZE // 2,
        )

    def update(self, dt: float):
        """Updates every frame"""
        # Move camera with arrow keys
        if self.keys[key.UP] or self.keys[key.W]:
            self.camera.move(0, 1)
        if self.keys[key.DOWN] or self.keys[key.S]:
            self.camera.move(0, -1)
        if self.keys[key.LEFT] or self.keys[key.A]:
            self.camera.move(-1, 0)
        if self.keys[key.RIGHT] or self.keys[key.D]:
            self.camera.move(1, 0)

        scroll_y = self.input_manager.mouse.scroll_y

        if scroll_y < 0:
            self.camera.zoom_in(dt)
        if scroll_y > 0:
            self.camera.zoom_out(dt)
