"""
Game Window
"""
import pyglet
from pyglet.window import key, mouse
import math

from . import constants
from . import resources
from .camera import Camera
from .world_controller import WorldController


class GameWindow(pyglet.window.Window):
    """The game window"""

    def __init__(
        self,
        width=constants.WINDOW_WIDTH,
        height=constants.WINDOW_HEIGHT,
        *args,
        **kwargs,
    ):
        super().__init__(width, height, *args, **kwargs)

        self.camera = Camera(
            self,
            speed=2.0,
            zoom_speed=1.1,
            min_zoom=4.0,
            max_zoom=8.0,
            center=True,
        )
        self.gui_camera = Camera(self)

        self.batch = pyglet.graphics.Batch()
        self.gui_batch = pyglet.graphics.Batch()

        self.tile_group = pyglet.graphics.OrderedGroup(0)
        self.ui_group = pyglet.graphics.OrderedGroup(1)

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.push_handlers(self.on_key_press)

        self.fps_display = pyglet.window.FPSDisplay(self)

        self.world_controller = WorldController(self.batch, self.tile_group)

        # Initialize camera position to middle of the world
        self.camera.position = (
            self.world_controller.world.width * constants.TILE_SIZE // 2,
            self.world_controller.world.height * constants.TILE_SIZE // 2,
        )

        self.tile_label = pyglet.text.Label("(0, 0)", x=10, y=50, batch=self.gui_batch)

        self.tile_highlighter = pyglet.sprite.Sprite(
            resources.tile_highlighter,
            batch=self.batch,
            group=self.ui_group,
        )
        self.tile_highlighter.visible = False

        self.highligted_tiles = []

        self.dragging_started_at = (0, 0)
        self.dragging = False

    def on_draw(self):
        self.clear()

        with self.camera:
            self.batch.draw()

        with self.gui_camera:
            self.gui_batch.draw()

        self.fps_display.draw()

    def screen_to_world_point(self, x: int, y: int) -> tuple[int, int]:
        # Potentially move to camera class
        world_x = (
            x / constants.TILE_SIZE / self.camera.zoom
            + self.camera.x / constants.TILE_SIZE
            - self.width // 2 / constants.TILE_SIZE / self.camera.zoom
        )
        world_y = (
            y / constants.TILE_SIZE / self.camera.zoom
            + self.camera.y / constants.TILE_SIZE
            - self.height // 2 / constants.TILE_SIZE / self.camera.zoom
        )
        return math.floor(world_x), math.floor(world_y)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            # return True so that the game does not exit
            return True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.highligted_tiles.clear()

    def on_mouse_motion(self, x, y, dx, dy):
        if not len(self.highligted_tiles):
            world_x, world_y = self.screen_to_world_point(x, y)
            tile = self.world_controller.world.get_tile_at(world_x, world_y)
            if tile:
                tile_type = tile.type
                self.tile_label.text = f"Tile: ({world_x}, {world_y}), {tile_type}"
                self.tile_highlighter.visible = True
                self.tile_highlighter.x = world_x * constants.TILE_SIZE
                self.tile_highlighter.y = world_y * constants.TILE_SIZE
            else:
                self.tile_label.text = ""
                self.tile_highlighter.visible = False
        else:
            self.tile_label.text = ""
            self.tile_highlighter.visible = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragging:
            dragging_ended_at = (x, y)
            start_tile_pos = self.screen_to_world_point(
                self.dragging_started_at[0], self.dragging_started_at[1]
            )
            end_tile_pos = self.screen_to_world_point(
                dragging_ended_at[0], dragging_ended_at[1]
            )

            if start_tile_pos[0] > end_tile_pos[0]:
                temp = start_tile_pos[0]
                start_tile_pos = (end_tile_pos[0], start_tile_pos[1])
                end_tile_pos = (temp, end_tile_pos[1])

            if start_tile_pos[1] > end_tile_pos[1]:
                temp = start_tile_pos[1]
                start_tile_pos = (start_tile_pos[0], end_tile_pos[1])
                end_tile_pos = (end_tile_pos[0], temp)

            start_tile = self.world_controller.world.get_tile_at(*start_tile_pos)
            end_tile = self.world_controller.world.get_tile_at(*end_tile_pos)

            if not start_tile or not end_tile:
                return

            self.highligted_tiles.clear()
            for tile_x in range(start_tile_pos[0], end_tile_pos[0] + 1):
                for tile_y in range(start_tile_pos[1], end_tile_pos[1] + 1):
                    sprite = pyglet.sprite.Sprite(
                        resources.tile_highlighter,
                        batch=self.batch,
                        group=self.ui_group,
                    )
                    sprite.x = tile_x * constants.TILE_SIZE
                    sprite.y = tile_y * constants.TILE_SIZE
                    self.highligted_tiles.append(sprite)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.dragging = True
            self.dragging_started_at = (x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.dragging = False

            dragging_ended_at = (x, y)
            start_tile_pos = self.screen_to_world_point(
                self.dragging_started_at[0], self.dragging_started_at[1]
            )
            end_tile_pos = self.screen_to_world_point(
                dragging_ended_at[0], dragging_ended_at[1]
            )

            if start_tile_pos[0] > end_tile_pos[0]:
                temp = start_tile_pos[0]
                start_tile_pos = (end_tile_pos[0], start_tile_pos[1])
                end_tile_pos = (temp, end_tile_pos[1])

            if start_tile_pos[1] > end_tile_pos[1]:
                temp = start_tile_pos[1]
                start_tile_pos = (start_tile_pos[0], end_tile_pos[1])
                end_tile_pos = (end_tile_pos[0], temp)

            start_tile = self.world_controller.world.get_tile_at(*start_tile_pos)
            end_tile = self.world_controller.world.get_tile_at(*end_tile_pos)

            if not start_tile or not end_tile:
                return

            self.highligted_tiles.clear()
            for tile_x in range(start_tile_pos[0], end_tile_pos[0] + 1):
                for tile_y in range(start_tile_pos[1], end_tile_pos[1] + 1):
                    sprite = pyglet.sprite.Sprite(
                        resources.tile_highlighter,
                        batch=self.batch,
                        group=self.ui_group,
                    )
                    sprite.x = tile_x * constants.TILE_SIZE
                    sprite.y = tile_y * constants.TILE_SIZE
                    self.highligted_tiles.append(sprite)

        # scale_x = end_tile_pos[0] - start_tile_pos[0] + 1
        # scale_y = end_tile_pos[1] - start_tile_pos[1] + 1

        # self.tile_highlighter.visible = True
        # self.tile_highlighter.x = start_tile_pos[0] * constants.TILE_SIZE
        # self.tile_highlighter.y = start_tile_pos[1] * constants.TILE_SIZE
        # self.tile_highlighter.scale_x = scale_x
        # self.tile_highlighter.scale_y = scale_y

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y < 0:
            self.camera.zoom_in()
        if scroll_y > 0:
            self.camera.zoom_out()

    def update(self, dt: float):
        # Move camera with arrow keys
        if self.keys[key.UP] or self.keys[key.W]:
            self.camera.move(0, 1)
        if self.keys[key.DOWN] or self.keys[key.S]:
            self.camera.move(0, -1)
        if self.keys[key.LEFT] or self.keys[key.A]:
            self.camera.move(-1, 0)
        if self.keys[key.RIGHT] or self.keys[key.D]:
            self.camera.move(1, 0)
