"""
Game Window
"""
import pyglet
from pyglet.window import key, mouse

from . import constants
from .background_manager import BackgroundManager
from .camera_manager import CameraManager
from .input_manager import InputManager
from .gui_manager import GUIManager
from .sprite_manager import SpriteManager


class GameWindow(pyglet.window.Window):
    """
    Game Window
    """

    def __init__(
        self,
        width: int = constants.WINDOW_WIDTH,
        height: int = constants.WINDOW_HEIGHT,
        *args,
        **kwargs,
    ):
        super().__init__(width, height, *args, **kwargs)

    def init(
        self,
        background_manager: BackgroundManager,
        input_manager: InputManager,
        camera_manager: CameraManager,
        sprite_manager: SpriteManager,
        gui_manager: GUIManager,
    ) -> None:
        self.background_manager: BackgroundManager = background_manager
        self.input_manager: InputManager = input_manager
        self.camera_manager: CameraManager = camera_manager
        self.sprite_manager: SpriteManager = sprite_manager
        self.gui_manager: GUIManager = gui_manager
        self.keys = key.KeyStateHandler()
        self.mouse_buttons = mouse.MouseStateHandler()
        self.register_push_handlers()

    def register_push_handlers(self) -> None:
        self.push_handlers(self.keys)
        self.push_handlers(self.mouse_buttons)
        self.push_handlers(self.on_key_press)

    def update(self, dt: float) -> None:
        pass

    def on_draw(self):
        self.clear()

        with self.camera_manager.background_camera:
            self.background_manager.batch.draw()

        with self.camera_manager.camera:
            self.sprite_manager.batch.draw()

        with self.camera_manager.gui_camera:
            self.gui_manager.batch.draw()

        self.gui_manager.fps_display.draw()

    # TODO: move to input manager
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            # return True so that the game does not exit
            return True

    # Mouse Events
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.input_manager.mouse.position = x, y
        pass

    def on_mouse_enter(self, x, y):
        # self.input_manager.mouse.position = x, y
        pass

    def on_mouse_leave(self, x, y):
        # self.input_manager.mouse.position = x, y
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.input_manager.mouse.position = x, y

    def on_mouse_press(self, x, y, button, modifiers):
        # self.input_manager.mouse.position = x, y
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        # self.input_manager.mouse.position = x, y
        pass

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # self.input_manager.mouse.position = x, y
        self.input_manager.mouse.scroll = scroll_x, scroll_y
