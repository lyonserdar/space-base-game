"""
Structure data class, installed objects like walls
"""
from .tile import Tile


class Structure:
    """
    Structure data class
    """

    def __init__(
        self,
        type_: str = "",
        movement_speed: float = 0.0,
        width: int = 1,
        height: int = 1,
    ):
        self.type_ = type_
        self.movement_speed = movement_speed
        self.width = width
        self.height = height
        self.tiles: list[Tile] = []

        # TODO: Implement larger structures
        # TODO: Implement object rotation

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
            width,
            height,
        )
        return blueprint

    @staticmethod
    def build_blueprint(blueprint: "Structure", tile: Tile) -> "Structure":
        structure = Structure(
            blueprint.type_,
            blueprint.movement_speed,
            blueprint.width,
            blueprint.height,
        )

        # TODO: fill the tiles list
        structure.tiles.append(tile)

        return structure
