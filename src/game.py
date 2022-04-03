"""
Game
"""
import pyglet

from .game_window import GameWindow
from .background_manager import BackgroundManager
from .camera_manager import CameraManager
from .input_manager import InputManager
from .gui_manager import GUIManager
from .world_manager import WorldManager
from .sound_manager import SoundManager
from .sprite_manager import SpriteManager
from .build_mode_manager import BuildModeManager


class Game:
    """
    Game
    """

    def __init__(self):
        self.window = GameWindow()
        self.background_manager: BackgroundManager = BackgroundManager()
        self.input_manager: InputManager = InputManager()
        self.world_manager: WorldManager = WorldManager()
        self.camera_manager: CameraManager = CameraManager()
        self.gui_manager: GUIManager = GUIManager()
        self.sound_manager: SoundManager = SoundManager()
        self.sprite_manager: SpriteManager = SpriteManager()
        self.build_mode_manager: BuildModeManager = BuildModeManager()

        self.managers = [
            self.background_manager,
            self.input_manager,
            self.world_manager,
            self.camera_manager,
            self.gui_manager,
            self.sound_manager,
            self.sprite_manager,
            self.build_mode_manager,
        ]

        self.initialize_managers()
        self.register_push_handlers()

    def initialize_managers(self):
        self.window.init(
            self.background_manager,
            self.input_manager,
            self.camera_manager,
            self.sprite_manager,
            self.gui_manager,
        )
        self.background_manager.init()
        self.input_manager.init()
        self.world_manager.init()
        self.camera_manager.init(self.input_manager, self.window)
        self.gui_manager.init(self.window, self.input_manager)
        self.sound_manager.init(self.world_manager)
        self.sprite_manager.init(self.world_manager)
        self.build_mode_manager.init(
            self.input_manager,
            self.camera_manager,
            self.world_manager,
            self.gui_manager,
            self.sprite_manager,
        )

    def register_push_handlers(self) -> None:
        for manager in self.managers:
            self.window.push_handlers(manager.keys)
            self.window.push_handlers(manager.mouse_buttons)

    # Pyglet Window Methods
    def update(self, dt: float):
        self.window.update(dt)

        for manager in self.managers:
            manager.update(dt)

        # Reset the mouse scroll
        # TODO: There might be a better place for this
        self.input_manager.mouse.scroll = 0, 0

        # DEBUG
        if self.world_manager.world.jobs:
            job = self.world_manager.world.jobs[0]
            job.do_work(1)
