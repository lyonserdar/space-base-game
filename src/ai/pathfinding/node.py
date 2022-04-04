"""
Node
"""
from typing import Generic


class Node(Generic[T]):
    """
    Node
    """

    def __init__(self, data: T):
        self.data: T = data
        self.edges: list["Edge"] = []
