from backend.genome import Genome
from utility.enums import *
from utility.vector import Vector


class Piece:
    def __init__(self, genome: Genome, color: Colors, is_pawn: bool = False, is_king: bool = False):
        self.genome = genome
        self.color = color
        self.is_pawn = is_pawn
        self.is_king = is_king

    def set_color(self, color: Colors):
        self.color = color

    def set_genome(self, genome: Genome):
        self.genome = genome

    def copy(self):
        return Piece(self.genome, self.color, self.is_pawn, self.is_king)

    def __repr__(self):
        return f"Piece(genome:{self.genome.hash()}, color:{self.color}, is pawn:{self.is_pawn}, is king:{self.is_king})"

    def get_debuffs(self):
        return self.genome.get_debuffs()

    def mutate(self):
        self.genome = self.genome.mutate()
    
    def _get_piece_owners(self, chessboard ,colour: Colors) -> dict[Vector, Players]:
        ans: dict[Vector, Players] = {}

        for (position, piece) in chessboard.items():
            ans[position] = Players.ME if piece.color == colour else Players.OPPONENT

        return ans

    def get_moves(self, board: dict[Vector, Players], coords: Vector):
        # genome can't see colour, only wheter it's our piece or not
        preprocessed_board = self._get_piece_owners(board, self.color)

        moves = self.genome.get_moves(preprocessed_board, coords)

        # filter moves according to debuffs

        debuffs = self.get_debuffs()

        if DebuffCodons.FORWARD_ONLY in debuffs:
            if self.color == Colors.WHITE:
                moves = [x for x in moves if x.to_position.y > x.original_position.y]
            else:
                moves=[x for x in moves if x.to_position.y < x.original_position.y]

        if DebuffCodons.ONLY_CAN_COLOR_DIFFERENT_COLOR in debuffs:
            moves=[x for x in moves if x.to_position.parity() != x.original_position.parity()]

        if DebuffCodons.ONLY_CAN_COLOR_SAME_COLOR in debuffs:
            moves=[x for x in moves if x.to_position.parity() == x.original_position.parity()]

        if DebuffCodons.ONLY_CAN_COLOR_NEIGHBOURS in debuffs:
            moves=[x for x in moves if abs(x.to_position.x - x.original_position.x) <= 1 and abs(x.to_position.y - x.original_position.y) <= 1]
        
        return moves