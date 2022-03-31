"""
Game Window
"""
import pyglet
from pyglet.window import key, mouse
import math

from . import constants
from . import resources
from .camera import Camera
from .world_manager import WorldManager
from .sound_manager import SoundManager
from .sprite_manager import SpriteManager
from .tile import Tile, TileType
from .structure import Structure
from .job import Job


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
            min_zoom=1.0,
            max_zoom=8.0,
            center=True,
        )
        self.gui_camera = Camera(self)

        self.batch = pyglet.graphics.Batch()
        self.gui_batch = pyglet.graphics.Batch()

        self.background_group = pyglet.graphics.OrderedGroup(0)
        self.forground_group = pyglet.graphics.OrderedGroup(1)
        self.gui_group = pyglet.graphics.OrderedGroup(2)

        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.push_handlers(self.on_key_press)

        self.fps_display = pyglet.window.FPSDisplay(self)

        self.world_manager: WorldManager = WorldManager()
        self.sound_manager: SoundManager = SoundManager(self.world_manager)
        self.sprite_manager: SpriteManager = SpriteManager(
            self.world_manager,
            self.batch,
            self.background_group,
            self.forground_group,
        )

        # Initialize camera position to middle of the world
        self.camera.position = (
            self.world_manager.world.width * constants.TILE_SIZE // 2,
            self.world_manager.world.height * constants.TILE_SIZE // 2,
        )

        self.tile_label = pyglet.text.Label("(0, 0)", x=10, y=50, batch=self.gui_batch)

        self.tile_highlighter = pyglet.sprite.Sprite(
            resources.tile_highlighter,
            batch=self.batch,
            group=self.gui_group,
        )
        self.tile_highlighter.visible = False

        # TODO: move this to its own file
        # TODO: use pooling so that it's more efficient
        self.highligted_tiles = {}

        self.dragging_started_at = (0, 0)
        self.draggind_started_at_tile = None
        self.dragging = False

        self.build_mode_type = None

    def update_hover_tile(self, x, y):
        world_x, world_y = self.camera.screen_to_world_point(x, y)
        tile = self.world_manager.world.get_tile_at(world_x, world_y)
        if tile:
            tile_type = tile.type
            self.tile_label.text = f"Tile: ({world_x}, {world_y}), {tile_type}"
            self.tile_highlighter.visible = True
            self.tile_highlighter.x = world_x * constants.TILE_SIZE
            self.tile_highlighter.y = world_y * constants.TILE_SIZE
        else:
            self.tile_label.text = ""
            self.tile_highlighter.visible = False

    # Pyglet Window Methods
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

    def on_draw(self):
        self.clear()

        with self.camera:
            self.batch.draw()

        with self.gui_camera:
            self.gui_batch.draw()

        self.fps_display.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            # return True so that the game does not exit
            return True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.highligted_tiles.clear()
            self.build_mode_type = None
        if symbol == key._1:
            self.build_mode_type = TileType.EMPTY
        if symbol == key._2:
            self.build_mode_type = TileType.FLOOR
        if symbol == key._3:
            self.build_mode_type = "wall"

    def on_mouse_motion(self, x, y, dx, dy):
        if not len(self.highligted_tiles):
            self.update_hover_tile(x, y)
        else:
            self.tile_label.text = ""
            self.tile_highlighter.visible = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # TODO: Fix the bug when world moves the selection is not correct
        if self.dragging:
            dragging_ended_at = (x, y)
            start_tile_pos = self.camera.screen_to_world_point(
                self.dragging_started_at[0], self.dragging_started_at[1]
            )
            end_tile_pos = self.camera.screen_to_world_point(
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

            start_tile = self.world_manager.world.get_tile_at(*start_tile_pos)
            end_tile = self.world_manager.world.get_tile_at(*end_tile_pos)

            # self.highligted_tiles.clear()
            keys_to_delete = []
            for tile_sprite in self.highligted_tiles:
                if (
                    tile_sprite[0] < start_tile_pos[0]
                    or tile_sprite[0] > end_tile_pos[0]
                    or tile_sprite[1] < start_tile_pos[1]
                    or tile_sprite[1] > end_tile_pos[1]
                ):
                    keys_to_delete.append(tile_sprite)

            for key in keys_to_delete:
                del self.highligted_tiles[key]

            for tile_x in range(start_tile_pos[0], end_tile_pos[0] + 1):
                for tile_y in range(start_tile_pos[1], end_tile_pos[1] + 1):
                    tile = self.world_manager.world.get_tile_at(tile_x, tile_y)
                    if tile:
                        if (tile_x, tile_y) not in self.highligted_tiles:
                            sprite = pyglet.sprite.Sprite(
                                resources.tile_highlighter,
                                batch=self.batch,
                                group=self.gui_group,
                            )
                            sprite.x = tile_x * constants.TILE_SIZE
                            sprite.y = tile_y * constants.TILE_SIZE
                            self.highligted_tiles[(tile_x, tile_y)] = sprite

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:

            self.dragging = True
            self.dragging_started_at = (x, y)
            tile_x, tile_y = self.camera.screen_to_world_point(x, y)
            self.draggind_started_at_tile = self.world_manager.world.tiles[
                (tile_x, tile_y)
            ]
            self.tile_highlighter.visible = False

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.dragging = False

            dragging_ended_at = (x, y)
            start_tile_pos = self.camera.screen_to_world_point(
                self.dragging_started_at[0], self.dragging_started_at[1]
            )
            end_tile_pos = self.camera.screen_to_world_point(
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

            start_tile = self.world_manager.world.get_tile_at(*start_tile_pos)
            end_tile = self.world_manager.world.get_tile_at(*end_tile_pos)

            self.highligted_tiles.clear()

            for tile_x in range(start_tile_pos[0], end_tile_pos[0] + 1):
                for tile_y in range(start_tile_pos[1], end_tile_pos[1] + 1):
                    tile = self.world_manager.world.get_tile_at(tile_x, tile_y)
                    if tile:

                        if self.build_mode_type:
                            # TODO: jobs for tile types like floor
                            if isinstance(self.build_mode_type, TileType):
                                # Change the tile type
                                self.world_manager.world.tiles[
                                    (tile_x, tile_y)
                                ].type = self.build_mode_type

                            if isinstance(self.build_mode_type, str):
                                # Build Structure or Furniture
                                structure_type = self.build_mode_type
                                # Check if already exists at the tile
                                if not any(
                                    job
                                    for job in self.world_manager.world.jobs
                                    if job.tile == tile
                                ):
                                    # Check if its a valid positon for the structure
                                    if self.world_manager.world.is_structure_valid_position(
                                        structure_type, tile
                                    ):
                                        job = Job(
                                            tile,
                                            1,
                                            # lambda: self.world_manager.world.place_structure(
                                            # structure_type, tile
                                            # ),
                                        )
                                        job.unsubscribe_on_tile_completed(
                                            self.world_manager.world.place_structure
                                        )

                                        self.world_manager.world.jobs.append(job)
                                        job.do_work(1)

            self.update_hover_tile(x, y)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y < 0:
            self.camera.zoom_in()
        if scroll_y > 0:
            self.camera.zoom_out()
