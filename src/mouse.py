"""
Mouse class
"""


class Mouse:
    """
    Mouse class
    """

    def __init__(self):
        self.x: int = 0
        self.y: int = 0

        self.scroll_x: int = 0
        self.scroll_y: int = 0

    @property
    def position(self) -> tuple:
        return self.x, self.y

    @position.setter
    def position(self, value: tuple[int, int]) -> None:
        self.x, self.y = value

    @property
    def scroll(self) -> tuple:
        return self.scroll_x, self.scroll_y

    @scroll.setter
    def scroll(self, value: tuple) -> None:
        self.scroll_x, self.scroll_y = value
