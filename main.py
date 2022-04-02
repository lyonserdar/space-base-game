import pyglet

from src.game import Game


def main():
    game = Game()
    pyglet.clock.schedule(game.update)
    pyglet.app.run()


if __name__ == "__main__":
    main()
