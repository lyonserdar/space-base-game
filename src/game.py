"""
Game
"""
import pyglet
from .game_window import GameWindow

# from .managers import Managers


class Game:
    """
    Game
    """

    game_window = GameWindow()

    def __init__(self):
        pass

    # Pyglet Window Methods
    @classmethod
    def update(cls, dt: float):
        cls.game_window.update(dt)
        # Managers.update(dt)

        # DEBUG
        # if Managers.world_manager.world.jobs:
        #     job = Managers.world_manager.world.jobs[0]
        #     job.do_work(0.1)
