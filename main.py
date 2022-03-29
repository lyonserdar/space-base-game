import pyglet

from src.game_window import GameWindow


def main():
    game_window = GameWindow()
    pyglet.clock.schedule(game_window.update)
    pyglet.app.run()


if __name__ == "__main__":
    main()
