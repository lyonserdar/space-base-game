"""
Job class
"""
from .tile import Tile


class Job:
    """
    Job class
    """

    def __init__(
        self,
        tile: Tile,
        work_required: float,
        structure_type: str,
        # on_completed=None,
        # on_canceled=None,
    ):
        self.tile = tile
        self.work_required = work_required
        self.structure_type = structure_type
        # self.on_completed = on_completed
        # self.on_canceled = on_canceled

        self.work_remaining = self.work_required

        self._on_job_created_callbacks = set()
        self._on_job_completed_callbacks = set()

    # Subscriptions
    def subscribe_on_job_created(self, fn):
        self._on_job_created_callbacks.add(fn)

    def unsubscribe_on_job_created(self, fn):
        self._on_job_created_callbacks.remove(fn)

    def subscribe_on_job_completed(self, fn):
        self._on_job_completed_callbacks.add(fn)

    def unsubscribe_on_job_completed(self, fn):
        self._on_job_completed_callbacks.remove(fn)

    def do_work(self, amount: float = 0) -> None:
        self.work_remaining -= amount
        if self.work_remaining <= 0:
            self.complete_job()

    def complete_job(self) -> None:
        for callback in self._on_job_completed_callbacks:
            callback(self)

    def cancel_job(self) -> None:
        for callback in self._on_job_completed_callbacks:
            callback(self)
