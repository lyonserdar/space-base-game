"""
Game Window
"""
import pyglet
from pyglet.window import key, mouse

from . import constants
from .camera_manager import CameraManager
from .input_manager import InputManager
from .gui_manager import GUIManager
from .world_manager import WorldManager
from .sound_manager import SoundManager
from .sprite_manager import SpriteManager
from .build_mode_manager import BuildModeManager


class GameWindow(pyglet.window.Window):
    """
    Game Window
    """

    def __init__(
        self,
        width=constants.WINDOW_WIDTH,
        height=constants.WINDOW_HEIGHT,
        *args,
        **kwargs,
    ):
        super().__init__(width, height, *args, **kwargs)

        self.keys = key.KeyStateHandler()
        self.mouse_buttons = mouse.MouseStateHandler()

        self.input_manager: InputManager = InputManager()
        self.world_manager: WorldManager = WorldManager()
        self.camera_manager: CameraManager = CameraManager(
            self,
            self.input_manager,
            self.world_manager,
        )
        self.gui_manager: GUIManager = GUIManager(
            self,
            self.input_manager,
        )
        self.sound_manager: SoundManager = SoundManager(
            self.input_manager,
            self.world_manager,
        )
        self.sprite_manager: SpriteManager = SpriteManager(self.world_manager)
        self.build_mode_manager: BuildModeManager = BuildModeManager(
            self,
            self.input_manager,
            self.world_manager,
            self.camera_manager,
            self.gui_manager,
            self.sprite_manager,
        )

        self.register_push_handlers()

    def register_push_handlers(self):
        self.push_handlers(self.keys)
        self.push_handlers(self.mouse_buttons)
        self.push_handlers(self.on_key_press)

        self.push_handlers(self.input_manager.keys)
        self.push_handlers(self.input_manager.mouse_buttons)

    # Pyglet Window Methods
    def update(self, dt: float):
        self.input_manager.update(dt)
        self.world_manager.update(dt)
        self.camera_manager.update(dt)
        self.gui_manager.update(dt)
        self.sound_manager.update(dt)
        self.sprite_manager.update(dt)
        self.build_mode_manager.update(dt)

        print(self.input_manager.mouse.position)

        # Reset the mouse scroll
        # TODO: There might be a better place for this
        self.input_manager.mouse.scroll = 0, 0

    def on_draw(self):
        self.clear()

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
        self.build_mode_manager.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

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
        self.build_mode_manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        # self.input_manager.mouse.position = x, y
        self.build_mode_manager.on_mouse_release(x, y, button, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        # self.input_manager.mouse.position = x, y
        self.input_manager.mouse.scroll = scroll_x, scroll_y
