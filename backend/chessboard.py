from utility.enums import *
from backend.move_descriptor import MoveDescriptor
from backend.genome import Genome
from backend.piece import Piece
from utility.vector import Vector
from utility.constants import *
from backend.preset import Preset
from collections import namedtuple

PieceInfo = namedtuple(
    "PieceInfo", ["genome_hash", "color", "is_pawn", "is_king"])


class Chessboard:
    def __init__(self, sandbox: bool = False):
        self.chessboard: dict[Vector, Piece] = {}
        self.current_descriptors: dict[Vector, MoveDescriptor] = {}
        self.need_to_promote: bool = False
        self.turn_number: int = 0
        self.sandbox: bool = sandbox
        self.king_counts: dict[colors, int] = {
            colors.WHITE: 0, colors.BLACK: 0}

    def insert_piece(self, genome_hash: str, color: colors, position: Vector, is_pawn=False, is_king=False):
        assert self.sandbox, "insert_piece only available in sandbox, in real games use presets"
        genome = Genome.from_hash(genome_hash)
        piece = Piece(genome, color, is_pawn, is_king)
        self._insert_piece(piece, position)

    def erase_piece(self, pos: Vector):
        assert self.sandbox, "erase_piece only available in sandbox, in real games use presets"
        self._erase_piece(pos)

    def set_king(self, position: Vector):
        if not self.sandbox:
            assert self.turn_number == 0, "Can't set king after the game has begun."
        if position in self.chessboard:
            self.chessboard[position].is_king = True
            color = self.chessboard[position].color
            self.king_counts[color] += 1
        else:
            raise IndexError

    def _erase_piece(self, pos: Vector):
        if pos in self.chessboard:
            del self.chessboard[pos]
        else:
            raise IndexError

    def _insert_piece(self, piece: Piece, position: Vector):
        self.chessboard[position] = piece

    def get_piece_owners(self, colour: colors) -> dict[Vector, players]:
        ans: dict[Vector, players] = {}

        for i in self.chessboard:
            ans[i] = players.ME if self.chessboard[i].color == colour else players.OPPONENT

        return ans

    def get_moves(self, coords: Vector) -> list[MoveDescriptor]:
        # check if moves are already calculated
        if coords in self.current_descriptors:
            return self.current_descriptors[coords]

        # check if there is a piece at the given coords
        if coords not in self.chessboard:
            # raise Exception("No piece at given coordinates")
            return []

        color = self.chessboard[coords].color
        if not self.sandbox and color != self.get_current_player():
            return []

        # get simplified board to pass to genome
        board = self.get_piece_owners(self.chessboard[coords].color)
        genome = self.chessboard[coords].genome
        moves = genome.get_moves(board, coords)

        # save moves for future use
        self.current_descriptors[coords] = moves
        return moves

    def __repr__(self):
        return "Chessboard: " + "".join([f"{i}:{self.chessboard[i]}\n" for i in self.chessboard])

    def do_move(self, descriptor: MoveDescriptor) -> GameStatus:

        # check if its the correct player's turn

        color = self.chessboard[descriptor.original_position].color
        other_color = colors.WHITE if color == colors.BLACK else colors.BLACK

        if not self.sandbox:
            assert color == self.get_current_player(), "Wrong player's turn"

            # TODO: should this be mandatory?
            assert not self.need_to_promote, "Pawn promotion is required before making a move"
            assert self.king_counts[colors.WHITE], "There is no white king"
            assert self.king_counts[colors.BLACK], "There is no black king"

        assert descriptor.original_position in self.current_descriptors, "Invalid move descriptor"
        assert descriptor in self.current_descriptors[descriptor.original_position], "Invalid move descriptor"

        # TODO: figure out what to do with the king status, since it can be split, stolen, etc.
        # current status: it just gets copied - ofc unusable because if a move makes it disappear(its not captured but just disappears) player is still in the game

        from_pos = descriptor.original_position
        to_pos = descriptor.to_position

        # move piece
        piece_from_original_pos = self.chessboard[from_pos]
        piece_from_new_pos = self.chessboard[to_pos] if to_pos in self.chessboard else None

        # firstly, erase them
        if from_pos in self.chessboard:
            self.chessboard.pop(from_pos)

        if to_pos in self.chessboard:
            self.chessboard.pop(to_pos)

        # clone correct piece to correct position

        # TODO somehow refactor into something reasonable
        if descriptor.original_square_new_state[0] == which_piece.MINE:
            if piece_from_original_pos is not None:
                self.chessboard[from_pos] = piece_from_original_pos.copy()

        if descriptor.original_square_new_state[0] == which_piece.OPPONENTS:
            if piece_from_new_pos is not None:
                self.chessboard[from_pos] = piece_from_new_pos.copy()

        if descriptor.to_square_new_state[0] == which_piece.MINE:
            if piece_from_original_pos is not None:
                self.chessboard[to_pos] = piece_from_original_pos.copy()

        if descriptor.to_square_new_state[0] == which_piece.OPPONENTS:
            if piece_from_new_pos is not None:
                self.chessboard[to_pos] = piece_from_new_pos.copy()

        # recolor the pieces correctly
        if to_pos in self.chessboard:
            self.chessboard[to_pos].set_color(
                color if descriptor.to_square_new_state[1] == players.ME else other_color)
        if from_pos in self.chessboard:
            self.chessboard[from_pos].set_color(
                color if descriptor.original_square_new_state[1] == players.ME else other_color)

        self.turn_number += 1

        # board state has changed, descriptors are invalidated
        self.current_descriptors.clear()

        if to_pos in self.chessboard and self.chessboard[to_pos].is_pawn:
            if to_pos.y == 0 and self.chessboard[to_pos].color == colors.WHITE:
                self.need_to_promote = True
                return GameStatus.PROMOTION_POSSIBLE
            if to_pos.y == BOARD_Y-1 and self.chessboard[to_pos].color == colors.BLACK:
                self.need_to_promote = True
                return GameStatus.PROMOTION_POSSIBLE

            # so far ignore weird case when opponent pawn is moved into my home row and technically can promote

        return GameStatus.IN_PROGRESS

    def promote(self, position, new_genome: Genome) -> None:
        assert position in self.chessboard and self.chessboard[position].is_pawn, "Invalid promotion"
        color = self.chessboard[position].color
        assert (color == colors.WHITE and position.y == 0) or (
            color == colors.BLACK and position.y == BOARD_Y-1), "Invalid promotion"
        self.chessboard[position].set_genome(new_genome)
        self.need_to_promote = False

    def load_preset(self, preset: Preset | str, color: colors):
        if type(preset) == str: #if we are given a preset hash, we need to fetch it
            preset = Preset.fetch_preset(preset)
        if not self.sandbox:
            assert self.turn_number == 0

        if color == colors.WHITE:
            row = 0
        elif color == colors.BLACK:
            row = BOARD_Y-1
        else:
            raise Exception

        for i in range(len(preset.genomes)):
            pos = Vector(i, row)

            if not self.sandbox:
                assert pos not in self.chessboard, "Attempt to place preset piece on an existing piece."

            piece = Piece(preset.genomes[i], color)
            self._insert_piece(piece, pos)

        # pawns
        if color == colors.WHITE:
            row = 1
        elif color == colors.BLACK:
            row = BOARD_Y-2

        pawn = Piece(Genome(PAWN_DNA), color, is_pawn=True)
        for i in range(BOARD_X):
            pos = Vector(i, row)

            if not self.sandbox:
                assert pos not in self.chessboard, "Attempt to place preset piece on an existing piece."

            self._insert_piece(pawn, pos)

    def get_board_for_reading(self) -> list[list[None | PieceInfo]]:
        res = [[None for _ in range(BOARD_X)] for _ in range(BOARD_Y)]

        for i in self.chessboard:
            piece = self.chessboard[i]
            res[i.y][i.x] = PieceInfo(
                piece.genome.hash(), piece.color, piece.is_pawn, piece.is_king)

        return res

    def get_current_player(self):
        return colors.WHITE if self.turn_number % 2 == 0 else colors.BLACK
