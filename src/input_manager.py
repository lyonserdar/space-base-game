"""
Input Manager
"""
import pyglet
from pyglet.window import key, mouse

from .mouse import Mouse


class InputManager:
    """
    InputManager
    """

    def __init__(self):
        self.keys = key.KeyStateHandler()
        self.mouse_buttons = mouse.MouseStateHandler()

        self.mouse: Mouse = Mouse()

    def update(self, dt: float):
        pass
