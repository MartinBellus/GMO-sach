from backend.genome import Genome
from utility.enums import *


class Piece:
    def __init__(self, genome: Genome, color: colors, is_pawn: bool = False, is_king: bool = False):
        self.genome = genome
        self.color = color
        self.is_pawn = is_pawn
        self.is_king = is_king

    def set_color(self, color: colors):
        self.color = color

    def set_genome(self, genome: Genome):
        self.genome = genome

    def copy(self):
        # TODO which should really copy over?
        return Piece(self.genome, self.color, self.is_pawn, self.is_king)
    
    def __repr__(self):
        return f"Piece(genome:{self.genome.hash()}, color:{self.color}, is pawn:{self.is_pawn}, is king:{self.is_king})"
