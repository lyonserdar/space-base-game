"""
Build Mode Manager
"""
import pyglet
from pyglet.sprite import Sprite
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

        self.highligted_tiles: dict[Tile, Sprite] = {}
        self.draggind_started_at_tile: Tile = None
        self.dragging: bool = False

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
        x, y = self.input_manager.mouse.position

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

        if not self.dragging:
            if self.mouse_buttons[mouse.LEFT]:
                self.start_dragging(x, y)

        if self.dragging:
            self.update_highlighted_tiles(x, y)
            if not self.mouse_buttons[mouse.LEFT]:
                self.finilize_dragging(x, y)

    def start_dragging(self, x, y) -> None:
        self.dragging = True
        self.dragging_started_at = (x, y)
        x, y = self.camera_manager.camera.screen_to_world_point(x, y)
        self.draggind_started_at_tile = self.world_manager.world.get_tile_at(x, y)
        self.tile_highlighter.visible = False

    def update_highlighted_tiles(self, x, y) -> None:
        end_tile_pos = self.camera_manager.camera.screen_to_world_point(x, y)

        temp_pos_x = self.draggind_started_at_tile.x, end_tile_pos[0]
        temp_pos_y = self.draggind_started_at_tile.y, end_tile_pos[1]

        start_tile_pos = min(temp_pos_x), min(temp_pos_y)
        end_tile_pos = max(temp_pos_x), max(temp_pos_y)

        start_tile = self.world_manager.world.get_tile_at(*start_tile_pos)
        end_tile = self.world_manager.world.get_tile_at(*end_tile_pos)

        sprites_to_delete = []
        for tile in self.highligted_tiles:
            if (
                tile.x < start_tile.x
                or tile.x > end_tile.x
                or tile.y < start_tile.y
                or tile.y > end_tile.y
            ):
                sprites_to_delete.append(tile)

        for tile in sprites_to_delete:
            del self.highligted_tiles[tile]

        for tile_x in range(start_tile.x, end_tile.x + 1):
            for tile_y in range(start_tile.y, end_tile.y + 1):
                tile = self.world_manager.world.get_tile_at(tile_x, tile_y)
                if tile and tile not in self.highligted_tiles:
                    sprite = pyglet.sprite.Sprite(
                        resources.tile_highlighter,
                        batch=self.sprite_manager.batch,
                        group=self.sprite_manager.gui_group,
                    )
                    sprite.x = tile_x * constants.TILE_SIZE
                    sprite.y = tile_y * constants.TILE_SIZE
                    self.highligted_tiles[tile] = sprite

    def finilize_dragging(self, x, y) -> None:
        self.dragging = False

        for tile in self.highligted_tiles:
            if self.build_mode_type and isinstance(self.build_mode_type, str):
                if self.world_manager.world.is_structure_valid_position(
                    self.build_mode_type, tile
                ):
                    if not any(
                        job for job in self.world_manager.world.jobs if job.tile == tile
                    ):
                        job = Job(tile, 1, self.build_mode_type)
                        job.subscribe_on_job_completed(
                            self.world_manager.world.place_structure
                        )

                        self.world_manager.world.jobs.append(job)

        self.highligted_tiles.clear()
        self.update_hover_tile(x, y)
