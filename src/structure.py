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
        build_time: int = 10,
    ):
        self.type_: str = type_
        self.movement_speed: float = movement_speed
        self.tile: Tile = None
        self.width: int = width
        self.height: int = height
        self.connected_texture: bool = connected_texture
        self.layer_order: int = layer_order
        self.build_time: int = build_time

        self.constructed: bool = False

        # Valid placement
        self.structure_types_needs_to_be_under: list[str] = []

        self._on_changed_callbacks = set()

    # Subscriptions
    def subscribe_on_changed(self, fn) -> None:
        self._on_changed_callbacks.add(fn)

    def unsubscribe_on_structure_changed(self, fn) -> None:
        self._on_changed_callbacks.remove(fn)

    def is_valid_position(self, structures_at_tile: list["Structure"]) -> bool:
        if "empty" in self.structure_types_needs_to_be_under:
            if structures_at_tile:
                return False
            else:
                return True

        if self.type_ in (s.type_ for s in structures_at_tile):
            return False

        if self.structure_types_needs_to_be_under:
            for type_ in self.structure_types_needs_to_be_under:
                if type_ not in (s.type_ for s in structures_at_tile):
                    return False

        return True

    @staticmethod
    def create_blueprint(
        structure_types_needs_to_be_under: list[str],
        type_: str = "",
        movement_speed: float = 0.0,
        width: int = 1,
        height: int = 1,
        connected_texture: bool = False,
        build_time: int = 10,
    ) -> "Structure":
        """Creates the blueprint"""
        # TODO: maybe create a blueprint class
        blueprint = Structure(
            type_=type_,
            movement_speed=movement_speed,
            width=width,
            height=height,
            connected_texture=connected_texture,
            build_time=build_time,
        )

        blueprint.structure_types_needs_to_be_under = structure_types_needs_to_be_under

        return blueprint

    @staticmethod
    def build_blueprint(blueprint: "Structure", tile: Tile) -> "Structure":
        structure = Structure(
            type_=blueprint.type_,
            movement_speed=blueprint.movement_speed,
            width=blueprint.width,
            height=blueprint.height,
            connected_texture=blueprint.connected_texture,
        )

        # TODO: fill the tiles list
        structure.tile = tile
        structure.completed = True

        for callback in structure._on_changed_callbacks:
            callback(structure)

        return structure
