from enums import *

class MoveDescriptor:
    def __init__(self, original_position:(int,int), to_position:(int,int), square_from:(which_piece, players), square_to:(which_piece, players)):
        self.original_position = original_position
        self.to_position = to_position
        self.original_square_new_state = square_from
        self.to_square_new_state = square_to