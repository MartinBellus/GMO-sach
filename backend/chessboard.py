from utility.enums import *
from backend.move_descriptor import MoveDescriptor
from backend.genome import Genome
from backend.piece import Piece
from utility.vector import Vector, inside_chessboard
from utility.constants import *
from backend.preset import Preset
from collections import namedtuple
from backend.chessclock import ChessClock
import random
import time

PieceInfo = namedtuple(
    "PieceInfo", ["genome_hash", "color", "is_pawn", "is_king"])


class Chessboard:
    def __init__(self, sandbox: bool = False):
        self.chessboard: dict[Vector, Piece] = dict()
        self.current_descriptors: dict[Vector, MoveDescriptor] = dict()
        self.need_to_promote: bool = False
        self.game_status: GameStatus = GameStatus.NOT_STARTED
        self.sandbox = sandbox
        if sandbox:
            self.game_status = GameStatus.LAB
        self.promotions: list[Vector] = list()
        self.turn_number: int = 0
        self.clock: ChessClock = ChessClock(TIME_PER_PLAYER)
        self._frozen: bool = False

    def _is_sandbox(self):
        return self.game_status == GameStatus.LAB

    def _real_game_assert(self, condition: bool, message: str):
        if self._is_sandbox():
            return
        assert condition, message

    def insert_piece(self, genome_hash: str, color: colors, position: Vector, is_pawn=False, is_king=False):
        # assert self.sandbox, "insert_piece only available in sandbox, in real games use presets"
        genome = Genome.from_hash(genome_hash)
        piece = Piece(genome, color, is_pawn, is_king)
        self._insert_piece(piece, position)

    def insert_piece_by_dna(self, dna: str, color: colors, position: Vector, is_pawn=False, is_king=False):
        # assert self.sandbox, "insert_piece only available in sandbox, in real games use presets"
        genome = Genome(dna)
        piece = Piece(genome, color, is_pawn, is_king)
        self._insert_piece(piece, position)

    def erase_piece(self, pos: Vector):
        self._real_game_assert(
            False, "erase_piece only available in sandbox, in real games use presets")
        self._erase_piece(pos)

    def toggle_king(self, position: Vector):
        self._real_game_assert(self.game_status == GameStatus.NOT_STARTED,
                               "Can't set king after the game has begun.")
        if position in self.chessboard:
            self.chessboard[position].is_king = not self.chessboard[position].is_king
        else:
            raise IndexError

    def _erase_piece(self, pos: Vector):
        if pos in self.chessboard:
            del self.chessboard[pos]
        else:
            raise IndexError

    def _insert_piece(self, piece: Piece, position: Vector):
        self.chessboard[position] = piece

    def _get_piece_owners(self, colour: colors) -> dict[Vector, players]:
        ans: dict[Vector, players] = {}

        for i in self.chessboard:
            ans[i] = players.ME if self.chessboard[i].color == colour else players.OPPONENT

        return ans

    def get_moves(self, coords: Vector, allowopponent:bool = False) -> list[MoveDescriptor]:
        # check if moves are already calculated
        if coords in self.current_descriptors and not self._is_sandbox():
            return self.current_descriptors[coords]

        # check if there is a piece at the given coords
        if coords not in self.chessboard:
            # raise Exception("No piece at given coordinates")
            return []

        self._real_game_assert(self.get_promotion() is None,
                               "Pawn promotion is required before making a move")

        piece = self.chessboard[coords]
        color = piece.color
        if not self._is_sandbox() and color != self.get_current_player() and not allowopponent:
            return []

        # get simplified board to pass to genome
        board = self._get_piece_owners(piece.color)
        genome = piece.genome
        moves = genome.get_moves(board, coords)

        debuffs = piece.get_debuffs()

        # apply debuffs
        if debuff_codons.FORWARD_ONLY in debuffs:
            if color == colors.WHITE:
                moves = [i for i in moves if i.to_position.y >
                         i.original_position.y]
            else:
                moves = [i for i in moves if i.to_position.y <
                         i.original_position.y]

        if debuff_codons.ONLY_CAN_COLOR_DIFFERENT_COLOR in debuffs:
            moves = [i for i in moves if i.original_position.parity()
                     != i.to_position.parity()]

        if debuff_codons.ONLY_CAN_COLOR_SAME_COLOR in debuffs:
            moves = [i for i in moves if i.original_position.parity()
                     == i.to_position.parity()]

        if debuff_codons.ONLY_CAN_COLOR_NEIGHBOURS in debuffs:
            moves = [i for i in moves if i.to_position not in self.chessboard or (abs(
                i.original_position.x - i.to_position.x) <= 1 and abs(i.original_position.y - i.to_position.y) <= 1)]

        # save moves for future use
        self.current_descriptors[coords] = moves
        return moves

    def __repr__(self):
        return "Chessboard: " + "".join([f"{i}:{self.chessboard[i]}\n" for i in self.chessboard])

    def count_kings(self, color: colors) -> int:
        ans = 0
        for i in self.chessboard:
            if self.chessboard[i].color == color and self.chessboard[i].is_king:
                ans += 1
        return ans

    def start_game(self):
        if self._is_sandbox():
            return
        self._real_game_assert(
            self.game_status == GameStatus.NOT_STARTED, "Game has already started")
        self._real_game_assert(self.turn_number == 0,
                               "Game has already started")
        self._real_game_assert(self.count_kings(
            colors.WHITE) >= 1, "White king is missing")
        self._real_game_assert(self.count_kings(
            colors.BLACK) >= 1, "Black king is missing")

        self.game_status = GameStatus.IN_PROGRESS
        self.clock.start(colors.WHITE)

    def do_move(self, descriptor: MoveDescriptor) -> GameStatus:

        # check if its the correct player's turn

        color = self.chessboard[descriptor.original_position].color
        other_color = colors.WHITE if color == colors.BLACK else colors.BLACK

        self._real_game_assert(
            color == self.get_current_player(), "Wrong player's turn")

        self._real_game_assert(self.get_promotion() is None,
                               "Pawn promotion is required before making a move")

        if self.get_status() not in (GameStatus.IN_PROGRESS, GameStatus.LAB):
            return self.get_status()

        assert descriptor.original_position in self.current_descriptors, "Invalid move descriptor"
        assert descriptor in self.current_descriptors[descriptor.original_position], "Invalid move descriptor"

        from_pos = descriptor.original_position
        to_pos = descriptor.to_position

        piece = self.chessboard[from_pos]

        # check if the move has deviation
        # TODO constants
        debuffs = piece.get_debuffs()
        if debuff_codons.RANDOM_MOVE_DEVIATION in debuffs:
            new_to_pos = Vector(to_pos.x + random.randint(-1, 1),
                                to_pos.y + random.randint(-1, 1))
            if inside_chessboard(new_to_pos):
                # fuck it, otherwise it stays the same
                to_pos = new_to_pos

        if debuff_codons.GAME_FREEZES_ON_MOVE in debuffs:
            self._frozen=True
            self.clock.add_time(color, -5)
            self.clock.add_time(other_color, 5)
        else:
            self._frozen=False

        if debuff_codons.RANDOM_MUTATION in debuffs:
            piece.mutate()

        # move piece
        piece_from_original_pos = self.chessboard[from_pos]
        piece_from_new_pos = self.chessboard[to_pos] if to_pos in self.chessboard else None

        # save original king counts
        white_kings = self.count_kings(colors.WHITE)
        black_kings = self.count_kings(colors.BLACK)

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

        self._calculate_promotions()

        # check for promotions

        self.clock.pause()
        self.clock.start(self.get_current_player())

        # if the number of kings decreases, the player loses
        white_loses = self.count_kings(colors.WHITE) < white_kings
        black_loses = self.count_kings(colors.BLACK) < black_kings

        if white_loses and black_loses:
            self._game_over(GameStatus.DRAW)
        elif white_loses:
            self._game_over(GameStatus.BLACK_WON)
        elif black_loses:
            self._game_over(GameStatus.WHITE_WON)

        return self.get_status()

    def _game_over(self, status: GameStatus) -> None:
        if self._is_sandbox():
            return
        self.game_status = status
        self.clock.pause()

    def _calculate_promotions(self) -> None:
        for (pos, piece) in self.chessboard.items():
            if piece.is_pawn:
                if (pos.y == 0 and piece.color == colors.BLACK) or (pos.y == BOARD_Y - 1 and piece.color == colors.WHITE):
                    self.promotions.append(pos)

    def get_promotion(self) -> tuple[Vector, colors] | None:
        if self.promotions:
            pos = self.promotions[0]
            return (pos, self.chessboard[pos].color)
        else:
            return None

    def promote(self, position, new_genome_hash: str) -> None:
        assert self.get_promotion is not None, "No promotions available"
        assert position == self.promotions[0], "Invalid promotion position"

        self._frozen=False

        self.clock.pause()

        old_piece = self.chessboard[position]

        new_genome = Genome.from_hash(new_genome_hash)

        self.chessboard[position] = Piece(
            new_genome, old_piece.color, is_king=old_piece.is_king)
        self.need_to_promote = False
        self.promotions.pop(0)

        self.clock.start(self.get_current_player())
    
    def is_frozen(self):
        return self._frozen

    def get_remaining_time(self, color: colors) -> float:
        return self.clock.get_time(color)

    def get_status(self):
        if self.game_status != GameStatus.IN_PROGRESS:
            return self.game_status

        if self.get_remaining_time(colors.WHITE) <= 0:
            self.game_status = GameStatus.BLACK_WON
        elif self.get_remaining_time(colors.BLACK) <= 0:
            self.game_status = GameStatus.WHITE_WON
        return self.game_status

    def load_preset(self, preset: Preset | str, color: colors):
        if type(preset) == str:  # if we are given a preset hash, we need to fetch it
            preset = Preset.fetch_preset(preset)
        self._real_game_assert(self.game_status == GameStatus.NOT_STARTED,
                               "Can't load preset after the game has begun.")

        if color == colors.WHITE:
            row = 0
        elif color == colors.BLACK:
            row = BOARD_Y-1
        else:
            raise Exception

        for i in range(len(preset.genomes)):
            pos = Vector(i, row)

            self._real_game_assert(
                pos not in self.chessboard, "Attempt to place preset piece on an existing piece.")

            piece = Piece(preset.genomes[i], color)
            self._insert_piece(piece, pos)

        # pawns
        if color == colors.WHITE:
            row = 1
        elif color == colors.BLACK:
            row = BOARD_Y-2

        pawn = Piece(Genome.from_hash("pesiak"), color, is_pawn=True)
        for i in range(BOARD_X):
            pos = Vector(i, row)

            self._real_game_assert(
                pos not in self.chessboard, "Attempt to place preset piece on an existing piece.")

            self._insert_piece(pawn.copy(), pos)

    def get_board_for_reading(self) -> list[list[None | PieceInfo]]:
        res = [[None for _ in range(BOARD_X)] for _ in range(BOARD_Y)]

        for i in self.chessboard:
            piece = self.chessboard[i]
            res[i.y][i.x] = PieceInfo(
                piece.genome.hash(), piece.color, piece.is_pawn, piece.is_king)

        return res

    def get_current_player(self):
        promotion = self.get_promotion()
        if promotion is not None:
            return promotion[1]
        return colors.WHITE if self.turn_number % 2 == 0 else colors.BLACK
