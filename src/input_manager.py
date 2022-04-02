"""
Input Manager
"""
import pyglet
from pyglet.window import key, mouse

from .mouse import Mouse

from .manager import Manager


class InputManager(Manager):
    """
    InputManager
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init(self) -> None:
        self.mouse: Mouse = Mouse()

    def update(self, dt: float):
        pass
