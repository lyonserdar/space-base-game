"""
Build Mode Manager
"""
import pyglet
from pyglet.window import key, mouse
import math

from . import constants
from . import resources
from .camera import Camera
from .camera_manager import CameraManager
from .input_manager import InputManager
from .gui_manager import GUIManager
from .world_manager import WorldManager
from .sound_manager import SoundManager
from .sprite_manager import SpriteManager
from .tile import Tile
from .structure import Structure
from .job import Job


class BuildModeManager:
    """
    Build Mode Manager
    """

    def __init__(
        self,
        window: pyglet.window.Window,
        input_manager: InputManager,
        world_manager: WorldManager,
        camera_manager: CameraManager,
        gui_manager: GUIManager,
        sprite_manager: SpriteManager,
    ):
        self.window: pyglet.window.Window = window
        self.input_manager: InputManager = input_manager
        self.world_manager: WorldManager = world_manager
        self.camera_manager: CameraManager = camera_manager
        self.gui_manager: GUIManager = gui_manager
        self.sprite_manager: SpriteManager = sprite_manager

        # TODO: potentially make the highlight tile not visible if zooming in or out
        self.tile_highlighter = pyglet.sprite.Sprite(
            resources.tile_highlighter,
            batch=self.sprite_manager.batch,
            group=self.sprite_manager.gui_group,
        )
        self.tile_highlighter.visible = False

        self.highligted_tiles = {}

        self.dragging_started_at = (0, 0)
        self.draggind_started_at_tile = None
        self.dragging = False

        self.build_mode_type: str = ""

        self.keys = self.input_manager.keys
        self.mouse_buttons = self.input_manager.mouse_buttons

    def update_hover_tile(self, x, y):
        # TODO: screen_to_world_point move to camera_manager
        world_x, world_y = self.camera_manager.camera.screen_to_world_point(x, y)
        tile = self.world_manager.world.get_tile_at(world_x, world_y)
        if tile:
            self.gui_manager.set_tile_info(f"({world_x}, {world_y})")
            self.tile_highlighter.visible = True
            self.tile_highlighter.x = world_x * constants.TILE_SIZE
            self.tile_highlighter.y = world_y * constants.TILE_SIZE
        else:
            self.gui_manager.set_tile_info("")
            self.tile_highlighter.visible = False

    def update(self, dt):
        self.mouse_buttons.values

        if self.keys[key.ESCAPE]:
            self.highligted_tiles.clear()
            self.build_mode_type = ""
        if self.keys[key._1]:
            self.build_mode_type = ""
        if self.keys[key._2]:
            self.build_mode_type = "floor"
        if self.keys[key._3]:
            self.build_mode_type = "wall"

        if not len(self.highligted_tiles):
            x, y = self.input_manager.mouse.position
            self.update_hover_tile(x, y)
        else:
            self.gui_manager.set_tile_info("")
            self.tile_highlighter.visible = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # TODO: Fix the bug when world moves the selection is not correct
        if self.dragging:
            dragging_ended_at = (x, y)
            start_tile_pos = self.camera_manager.camera.screen_to_world_point(
                self.dragging_started_at[0], self.dragging_started_at[1]
            )
            end_tile_pos = self.camera_manager.camera.screen_to_world_point(
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
                                batch=self.sprite_manager.batch,
                                group=self.sprite_manager.gui_group,
                            )
                            sprite.x = tile_x * constants.TILE_SIZE
                            sprite.y = tile_y * constants.TILE_SIZE
                            self.highligted_tiles[(tile_x, tile_y)] = sprite

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:

            self.dragging = True
            self.dragging_started_at = (x, y)
            tile_x, tile_y = self.camera_manager.camera.screen_to_world_point(x, y)
            self.draggind_started_at_tile = self.world_manager.world.tiles[
                (tile_x, tile_y)
            ]
            self.tile_highlighter.visible = False

    def on_mouse_release(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            self.dragging = False

            dragging_ended_at = (x, y)
            start_tile_pos = self.camera_manager.camera.screen_to_world_point(
                self.dragging_started_at[0], self.dragging_started_at[1]
            )
            end_tile_pos = self.camera_manager.camera.screen_to_world_point(
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
                        if self.build_mode_type and isinstance(
                            self.build_mode_type, str
                        ):
                            structure_type = self.build_mode_type
                            if self.world_manager.world.is_structure_valid_position(
                                structure_type, tile
                            ):
                                if not any(
                                    job
                                    for job in self.world_manager.world.jobs
                                    if job.tile == tile
                                ):
                                    job = Job(tile, 1, structure_type)
                                    job.subscribe_on_job_completed(
                                        self.world_manager.world.place_structure
                                    )

                                    self.world_manager.world.jobs.append(job)
                                    job.do_work(1)

            self.update_hover_tile(x, y)
