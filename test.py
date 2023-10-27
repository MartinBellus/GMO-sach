from chessboard import Chessboard
from genome import *
from piece import Piece
from time import sleep
from constants import *
import random
from preset import Preset


def print_chessboard(board):
    ans = [["."]*BOARD_X for i in range(BOARD_Y)]

    for i in board.chessboard:
        color = board.chessboard[i].color

        ans[i.y][i.x] = "W" if color == colors.WHITE else "B"

    for i in ans:
        print("".join(i))


rook_genome = "AHH HSH HAA CHA CHA CHA HHA SAS AAA AAA AAA".replace(" ", "")
genome = Genome(rook_genome)
genome.save()
hash=genome.hash()
board = Chessboard(sandbox=True)
pieces = []

preset = Preset([hash for i in range(BOARD_X)])
hsh=preset.hash()
preset.save()

pres=Preset.fetch_preset(hsh)
board.load_preset(pres, colors.WHITE)


while 1:
    print()
    print_chessboard(board)
    print()

    pos = Vector(random.randint(0, BOARD_X-1), random.randint(0, BOARD_Y-1))

    moves = board.get_moves(pos)

    if not moves:
        continue

    move = random.choice(moves)

    board.do_move(move)
    sleep(1)
