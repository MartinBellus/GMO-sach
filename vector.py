from enums import *
from constants import *


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __mul__(self, k):
        return Vector(self.x * k, self.y * k)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Vector({self.x},{self.y})"

    def parity(self) -> bool:
        return (self.x + self.y)%2


def inside_chessboard(position: Vector) -> bool:
    return 0 <= position.x and position.x < BOARD_X and 0 <= position.y and position.y < BOARD_Y
