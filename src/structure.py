"""
Structure data class, installed objects like walls
"""
from .tile import Tile, TileType


class Structure:
    """
    Structure data class
    """

    def __init__(
        self,
        type_: str = "",
        movement_speed: float = 0.0,
    ):
        self.type_ = type_
        self.movement_speed = movement_speed
        self.tile: Tile = None

        self._on_structure_changed_callbacks = set()

        self.is_valid_position = self.is_valid_position_default

    # Subscriptions
    def subscribe_on_structure_changed(self, fn):
        self._on_structure_changed_callbacks.add(fn)

    def unsubscribe_on_structure_changed(self, fn):
        self._on_structure_changed_callbacks.remove(fn)

    def is_valid_position_default(self, tile: Tile) -> bool:
        if tile._type == TileType.FLOOR:
            return True
        return False

    def is_valid_position_door(self, tile: Tile) -> bool:
        return True

    @staticmethod
    def create_blueprint(
        type_: str = "",
        movement_speed: float = 0.0,
        width: int = 1,
        height: int = 1,
    ) -> "Structure":
        """Creates the blueprint"""
        # TODO: maybe create a blueprint class
        blueprint = Structure(
            type_,
            movement_speed,
        )
        return blueprint

    @staticmethod
    def build_blueprint(blueprint: "Structure", tile: Tile) -> "Structure":
        if not blueprint.is_valid_position(tile):
            return None

        structure = Structure(
            blueprint.type_,
            blueprint.movement_speed,
        )

        # TODO: fill the tiles list
        structure.tile = tile

        for callback in structure._on_structure_changed_callbacks:
            callback(structure)

        return structure
