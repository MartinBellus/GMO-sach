from enums import *
from move_descriptor import MoveDescriptor
from genome import Genome


class Chessboard:
    def __init__(self):
        self.chessboard = [
            [None for _ in range(BOARD_X)] for _ in range(BOARD_Y)]
        self.current_descriptors = {}
        self.need_to_promote = False
        self.turn_number = 0

    def insert_piece(self, piece, x, y):
        self.chessboard[y][x] = piece

    def get_coloured_board(self, colour: colors) -> [[players]]:
        ans = [[None for _ in range(BOARD_X)] for _ in range(BOARD_Y)]
        for y in range(BOARD_Y):
            for x in range(BOARD_X):
                if self.chessboard[y][x] == None:
                    ans[y][x] = players.NONE
                else:
                    if self.chessboard[y][x].color == colour:
                        ans[y][x] = players.ME
                    else:
                        ans[y][x] = players.OPPONENT

        return ans

    def get_moves(self, x: int, y: int):
        # check if moves are already calculated
        if (x, y) in self.current_descriptors:
            return self.current_descriptors[(x, y)]

        # get simplified board to pass to genome
        board = self.get_coloured_board(self.chessboard[y][x].color)
        genome = self.chessboard[y][x].genome
        moves = genome.get_moves(board, x, y)

        # save moves for future use
        self.current_descriptors[(x, y)] = moves
        return moves

    def do_move(self, descriptor: MoveDescriptor) -> GameStatus:

        # check if its the correct player's turn

        color = self.chessboard[descriptor.original_position[1]
                                ][descriptor.original_position[0]].color

        assert (color == colors.WHITE and self.turn_number % 2 == 0) or (
            color == colors.BLACK and self.turn_number % 2 == 1), "Wrong player's turn"

        # TODO: should this be mandatory?
        assert not self.need_to_promote, "Pawn promotion is required before making a move"

        assert descriptor.original_position in self.current_descriptors, "Invalid move descriptor"
        assert descriptor in self.current_descriptors[descriptor.original_position], "Invalid move descriptor"

        # TODO: figure out what to do with the king status, since it can be split, stolen, etc.
        # current status: it just gets copied - ofc unusable because if a move makes it disappear(its not captured but just disappears) player is still in the game

        from_pos = descriptor.original_position
        to_pos = descriptor.to_position

        fromx, fromy = from_pos
        tox, toy = to_pos

        # move piece
        piece_from_original_pos = self.chessboard[fromy][fromx]
        piece_from_new_pos = self.chessboard[toy][tox]

        self.chessboard[fromy][fromx] = None
        self.chessboard[toy][tox] = None

        # clone correct piece to correct position
        if descriptor.original_square_new_state[0] == which_piece.MINE:
            self.chessboard[fromy][fromx] = piece_from_original_pos.copy()

        if descriptor.original_square_new_state[0] == which_piece.OPPONENTS:
            self.chessboard[fromy][fromx] = piece_from_new_pos.copy()

        if descriptor.to_square_new_state[0] == which_piece.MINE:
            self.chessboard[toy][tox] = piece_from_original_pos.copy()

        if descriptor.to_square_new_state[0] == which_piece.OPPONENTS:
            self.chessboard[toy][tox] = piece_from_new_pos.copy()

        # recolor the pieces correctly
        if self.chessboard[toy][tox] is not None:
            self.chessboard[toy][tox].set_color(
                descriptor.to_square_new_state[1])
        if self.chessboard[from_pos[1]][from_pos[0]] is not None:
            self.chessboard[from_pos[1]][from_pos[0]].set_color(
                descriptor.original_square_new_state[1])

        # board state has changed, descriptors are invalidated
        self.current_descriptors.clear()

        if self.chessboard[toy][tox] is not None and self.chessboard[toy][tox].is_pawn:
            if toy == 0 and self.chessboard[toy][tox].color == colors.WHITE:
                self.need_to_promote = True
                return GameStatus.PROMOTION_POSSIBLE
            if toy == BOARD_Y-1 and self.chessboard[toy][tox].color == colors.BLACK:
                self.need_to_promote = True
                return GameStatus.PROMOTION_POSSIBLE

            # so far ignore weird case when opponent pawn is moved into my home row and technically can promote

        return GameStatus.IN_PROGRESS

    def promote(self, x: int, y: int, new_genome: Genome) -> None:
        assert self.chessboard[y][x] is not None and self.chessboard[y][x].is_pawn, "Invalid promotion"
        color = self.chessboard[y][x].color
        assert (color == colors.WHITE and y == 0) or (
            color == colors.BLACK and y == BOARD_Y-1), "Invalid promotion"
        self.chessboard[y][x].set_genome(new_genome)
        self.need_to_promote = False
