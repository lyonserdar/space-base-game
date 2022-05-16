"""
Character
"""
from . import constants
from .job import Job
from .tile import Tile


class Character:
    """
    Character
    """

    def __init__(
        self,
        tile: Tile,
        speed: float = 10.0,
        build_speed: float = 10.0,
    ):
        self._x: float = 0
        self._y: float = 0
        self.tile: Tile = tile
        self.speed: float = speed
        self.build_speed: float = build_speed

        self.job: Job | None = None
        self.path: list[Tile] = []

        self.current_tile: Tile = tile
        self.destination_tile: Tile = None

        self.movement_percentage: float = 0.0  # Between 0.0 and 1.0

    # @property
    # def x(self) -> float:
    #     return Character.lerp(
    #         self.current_tile.x, self.destination_tile.x, self.movement_percentage
    #     )

    # @property
    # def y(self) -> float:
    #     return Character.lerp(
    #         self.current_tile.y, self.destination_tile.y, self.movement_percentage
    #     )

    @staticmethod
    def lerp(current: float, destination: float, percentage: float) -> float:
        return (percentage * destination) + ((1 - percentage) * current)

    def assign_job(self, job: Job, path: list[Tile]) -> None:
        self.job = job
        self.path = path
        job.subscribe_on_job_completed(self.on_job_completed)

    def remove_job(self) -> None:
        self.job = None

    def on_job_completed(self, job: Job) -> None:
        self.remove_job()

    def update(self, dt: float) -> None:
        if self.job:
            print("path", self.path)
            if self.path:
                if (
                    self.current_tile == self.destination_tile
                    or not self.destination_tile
                ):
                    # self.destination_tile = self.job.tile
                    self.destination_tile = self.path.pop()

            # if self.current_tile == self.destination_tile:
            if self.current_tile == self.job.tile:
                if self.job:
                    self.job.do_work(self.build_speed * dt)
                return

            distance_to_travel = (
                (self.current_tile.x - self.destination_tile.x) ** 2
                + (self.current_tile.y - self.destination_tile.y) ** 2
            ) ** (1 / 2)

            character_can_travel = self.speed * dt

            percentage_can_travel = character_can_travel / distance_to_travel

            self.movement_percentage += percentage_can_travel

            if self.movement_percentage >= 1.0:
                self.current_tile = self.destination_tile
                self.movement_percentage = 0.0
