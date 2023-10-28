from utility.enums import *
from utility.vector import Vector

class MoveDescriptor:
    def __init__(self, original_position:Vector, to_position:Vector, square_from:(which_piece, players), square_to:(which_piece, players)):
        self.original_position = original_position
        self.to_position = to_position
        self.original_square_new_state = square_from
        self.to_square_new_state = square_to