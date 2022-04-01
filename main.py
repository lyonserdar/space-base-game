import pyglet

# from src.game_window import GameWindow
from src.game import Game


def main():
    # game_window = GameWindow()
    game = Game()
    pyglet.clock.schedule(Game.update)
    pyglet.app.run()


if __name__ == "__main__":
    main()
