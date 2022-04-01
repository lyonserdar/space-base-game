"""
Structure class
"""
from .tile import Tile


class Structure:
    """
    Structure class
    """

    def __init__(
        self,
        type_: str = "",
        movement_speed: float = 0.0,
        width: int = 1,
        height: int = 1,
        connected_texture: bool = False,
        layer_order: int = 0,  # background: 0, forground:1, gui: 2
    ):
        self.type_: str = type_
        self.movement_speed: float = movement_speed
        self.tile: Tile = None
        self.width: int = width
        self.height: int = height
        self.connected_texture: bool = connected_texture
        self.layer_order: int = layer_order

        self.constructed: bool = False

        self._on_changed_callbacks = set()

        self.is_valid_position = self.is_valid_position_default

    # Subscriptions
    def subscribe_on_changed(self, fn) -> None:
        self._on_changed_callbacks.add(fn)

    def unsubscribe_on_structure_changed(self, fn) -> None:
        self._on_changed_callbacks.remove(fn)

    def is_valid_position_default(self, list_of_structures: list["Structure"]) -> bool:
        # TODO: actually implement it
        return True

    def is_valid_position_wall(self, tile: Tile) -> bool:
        # TODO:
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
        connected_texture: bool = False,
    ) -> "Structure":
        """Creates the blueprint"""
        # TODO: maybe create a blueprint class
        blueprint = Structure(
            type_,
            movement_speed,
            width,
            height,
            connected_texture,
        )
        return blueprint

    @staticmethod
    def build_blueprint(blueprint: "Structure", tile: Tile) -> "Structure":
        structure = Structure(
            blueprint.type_,
            blueprint.movement_speed,
            blueprint.width,
            blueprint.height,
            blueprint.connected_texture,
        )

        # TODO: fill the tiles list
        structure.tile = tile
        structure.completed = True

        for callback in structure._on_changed_callbacks:
            callback(structure)

        return structure
