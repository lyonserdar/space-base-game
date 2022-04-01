"""
Camera class that allows scrolling and zooming.
Based on: pyglet/examples
"""
import pyglet
from pyglet.math import Vec2
import math

from . import constants


class Camera:
    """
    Camera that allows scrolling and zooming
    """

    def __init__(
        self,
        window: pyglet.window.Window,
        speed: float = 1.0,
        # zoom_speed: float = 1.25,
        min_zoom: int = 1.0,
        max_zoom: int = 10.0,
        center: bool = False,
    ):
        self.window = window
        self.speed = speed
        # self.zoom_speed = zoom_speed
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.center = center

        self.x: int = 0
        self.y: int = 0
        self._zoom: float = self.min_zoom

    @property
    def zoom(self) -> float:
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        # Clamp the zoom
        self._zoom = max(min(value, self.max_zoom), self.min_zoom)

    @property
    def position(self) -> Vec2:
        """Get the current camera position"""
        return Vec2(self.x, self.y)

    @position.setter
    def position(self, value: Vec2):
        """Set the camera position manually"""
        self.x, self.y = value

    def move(self, x, y) -> None:
        """Move the camera"""
        # TODO: Work on this later
        self.x += self.speed * x
        self.y += self.speed * y

    def zoom_in(self, dt) -> None:
        """Zooms in the camera"""
        # TODO: make the zoom smoother by making pixel increments
        # self.zoom += self.zoom_speed
        self.zoom += 1

    def zoom_out(self, dt) -> None:
        """Zooms out the camera"""
        # TODO: make the zoom smoother by making pixel increments
        # self.zoom -= self.zoom_speed * dt
        self.zoom -= 1

    def screen_to_world_point(self, x: int, y: int) -> tuple[int, int]:
        # Potentially move to camera class
        world_x = (
            x / constants.TILE_SIZE / self.zoom
            + self.x / constants.TILE_SIZE
            - self.window.width // 2 / constants.TILE_SIZE / self.zoom
        )
        world_y = (
            y / constants.TILE_SIZE / self.zoom
            + self.y / constants.TILE_SIZE
            - self.window.height // 2 / constants.TILE_SIZE / self.zoom
        )
        return math.floor(world_x), math.floor(world_y)

    def __enter__(self):
        offset_x = 0
        offset_y = 0

        if self.center:
            offset_x = self.window.width // 2
            offset_y = self.window.height // 2

        pyglet.gl.glTranslatef(
            -self.x * self._zoom + offset_x,
            -self.y * self._zoom + offset_y,
            0,
        )
        pyglet.gl.glScalef(self._zoom, self._zoom, 1)

    def __exit__(self, exception_type, exception_value, traceback):
        offset_x = 0
        offset_y = 0

        if self.center:
            offset_x = self.window.width // 2
            offset_y = self.window.height // 2

        pyglet.gl.glScalef(1 / self._zoom, 1 / self._zoom, 1)
        pyglet.gl.glTranslatef(
            self.x * self._zoom - offset_x,
            self.y * self._zoom - offset_y,
            0,
        )
