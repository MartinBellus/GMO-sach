from utility.enums import *
from utility.vector import Vector

"""
Describes a possible move in the game.
original_position: The position of the piece before the move
to_position: The position of the piece after the move
original_square_new_state: tuple (piece, player)
    piece: describes which piece will be copied on the original square after the move
    player: the owner of the piece
to_square_new_state: tuple (piece, player) - same as above
"""


class MoveDescriptor:
    def __init__(self, original_position: Vector, to_position: Vector, square_from: (WhosePieceEnum, Players), square_to: (WhosePieceEnum, Players)):
        self.original_position = original_position
        self.to_position = to_position
        self.original_square_new_state = square_from
        self.to_square_new_state = square_to
