"""
Manager abstract base class
"""
import pyglet
from pyglet.window import key, mouse
from abc import ABC, abstractmethod


class Manager(ABC):
    """
    Manager abstract base class
    """

    def __init__(self):
        self.keys = key.KeyStateHandler()
        self.mouse_buttons = mouse.MouseStateHandler()

    @abstractmethod
    def update(self, dt) -> None:
        ...
