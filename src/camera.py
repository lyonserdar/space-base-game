"""
Camera class that allows scrolling and zooming.
Based on: pyglet/examples
"""
import pyglet
from pyglet.math import Vec2


class Camera:
    """
    Camera that allows scrolling and zooming
    """

    def __init__(
        self,
        window: pyglet.window.Window,
        speed: float = 1.0,
        zoom_speed: float = 1.25,
        min_zoom: float = 1.0,
        max_zoom: float = 10.0,
        center: bool = False,
    ):
        self.window = window
        self.speed = speed
        self.zoom_speed = zoom_speed
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

    def zoom_in(self) -> None:
        """Zooms in the camera"""
        self.zoom += self.zoom_speed

    def zoom_out(self) -> None:
        """Zooms out the camera"""
        self.zoom -= self.zoom_speed

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
