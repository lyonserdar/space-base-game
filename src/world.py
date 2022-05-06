"""
Word class for world data
"""
from collections import deque
from itertools import chain
from typing import Callable

from .character import Character
from .job import Job
from .pathfinding import TileGraph
from .structure import Structure
from .tile import Tile


class World:
    """
    World class
    """

    def __init__(
        self,
        width: int = 100,
        height: int = 100,
    ):
        self.width: int = width
        self.height: int = height

        self.tiles: dict[(int, int), Tile] = {}
        self.blueprints: dict[str, Structure] = {}
        self.structures: dict[Tile, list[Structure]] = {}

        self.characters: list[Character] = []

        self._on_structure_changed_callbacks = set()
        self._on_job_created_callbacks = set()
        self._on_job_completed_callbacks = set()

        self.tile_graph: TileGraph = None

        # TODO: refactor to job manager
        self.jobs = deque()

        self.initialize()

        self.blueprints = {
            "floor": Structure.create_blueprint(
                structure_types_needs_to_be_under=["empty"],
                type_="floor",
                movement_speed=0.5,
                connected_texture=False,
                build_time=5,
            ),
            "wall": Structure.create_blueprint(
                structure_types_needs_to_be_under=["floor"],
                type_="wall",
                movement_speed=0.0,
                connected_texture=True,
                build_time=10,
            ),
        }

    # Subscriptions
    def subscribe_on_structure_changed(self, fn):
        self._on_structure_changed_callbacks.add(fn)

    def unsubscribe_on_structure_changed(self, fn):
        self._on_structure_changed_callbacks.remove(fn)

    def subscribe_on_job_created(self, fn):
        self._on_job_created_callbacks.add(fn)

    def unsubscribe_on_job_created(self, fn):
        self._on_job_created_callbacks.remove(fn)

    def subscribe_on_job_completed(self, fn):
        self._on_job_completed_callbacks.add(fn)

    def unsubscribe_on_job_completed(self, fn):
        self._on_job_completed_callbacks.remove(fn)

    def on_structure_changed(self, structure: Structure) -> None:
        for callback in self._on_structure_changed_callbacks:
            callback(structure)

    def on_job_created(self, job: Job) -> None:
        for callback in self._on_job_created_callbacks:
            callback(job)

    def on_job_completed(self, job: Job) -> None:
        self.place_structure(job)
        # self.jobs.remove(job)

        for callback in self._on_job_completed_callbacks:
            callback(job)

        self.tile_graph = TileGraph(self)

    def create_job(self, tile: Tile, structure_type: str) -> None:
        if not any(job for job in self.jobs if job.tile == tile):
            blueprint = self.blueprints[structure_type]
            job = Job(tile, blueprint)
            job.subscribe_on_job_created(self.on_job_created)
            job.subscribe_on_job_completed(self.on_job_completed)
            self.on_job_created(job)
            self.jobs.append(job)

    def initialize(self):
        for x in range(self.width):
            for y in range(self.height):
                tile = Tile(x, y)
                self.tiles[(x, y)] = tile
                self.structures[tile] = []

        self.characters.append(Character(self.get_tile_at(50, 50)))
        print("World Initialized")
        self.tile_graph = TileGraph(self)

    def get_tile_at(self, x: int, y: int) -> Tile | None:
        if (x, y) not in self.tiles:
            return None
        return self.tiles[(x, y)]

    def is_structure_valid_position(self, type_: str, tile: Tile) -> bool:
        return self.blueprints[type_].is_valid_position(self.structures[tile])

    def get_structure_neighbors(self, structure: Structure) -> list[Structure]:
        # TODO: Fix this for the new neighbor list system
        neighbors = []

        x = structure.tile.x
        y = structure.tile.y

        w = self.get_tile_at(x - 1, y + 0)
        n = self.get_tile_at(x + 0, y + 1)
        e = self.get_tile_at(x + 1, y + 0)
        s = self.get_tile_at(x + 0, y - 1)
        nw = self.get_tile_at(x - 1, y + 1)
        ne = self.get_tile_at(x + 1, y + 1)
        se = self.get_tile_at(x + 1, y - 1)
        sw = self.get_tile_at(x - 1, y - 1)

        if w in self.structures:
            neighbors.append(self.structures[w])
        if n in self.structures:
            neighbors.append(self.structures[n])
        if e in self.structures:
            neighbors.append(self.structures[e])
        if s in self.structures:
            neighbors.append(self.structures[s])
        if nw in self.structures:
            neighbors.append(self.structures[nw])
        if ne in self.structures:
            neighbors.append(self.structures[ne])
        if se in self.structures:
            neighbors.append(self.structures[se])
        if sw in self.structures:
            neighbors.append(self.structures[sw])

        return list(chain(*neighbors))

    def place_structure(self, job: Job) -> None:
        structure = Structure.build_blueprint(
            self.blueprints[job.structure_type], job.tile
        )
        structure.subscribe_on_changed(self.on_structure_changed)

        if structure:
            self.structures[job.tile].append(structure)

            neighbors = self.get_structure_neighbors(structure)
            for neighbor in neighbors:
                self.on_structure_changed(neighbor)

            self.on_structure_changed(structure)

    def update(self, dt) -> None:
        for character in self.characters:
            if not character.job:
                if self.jobs:
                    job = self.jobs.pop()
                    character.assign_job(job)
            character.update(dt)
