from frontend.chessboard import ChessboardUI
from frontend.genome_editor import EditorUI
from frontend.popups import InputPopup
from frontend.menu import Menu
from frontend.chessclock import ChessClockUI
from backend.chessboard import Chessboard
from utility.constants import *
from utility.enums import colors, GameStatus
from utility.vector import Vector
import tkinter

def nic():
    print("nic")

def set_kings():
    for x in range(BOARD_X):
        for y in range(BOARD_Y):
            try:
                cnt.set_king(Vector(x,y))
            except:
                pass
    ui.redraw_pieces()

if __name__ == "__main__":
    root = tkinter.Tk()
    cnt = Chessboard(1)
    ui = ChessboardUI(root,cnt,width=WIDTH,height=HEIGHT,bg="yellow")
    editor = EditorUI(root,ui,width=100,height=HEIGHT,bg="green")
    clock = ChessClockUI(root,cnt,height=HEIGHT,width= 100)
    a = [(f"test{i}",set_kings) for i in range(5)]
    a.append(("Start Game",lambda : ui.switch_state(GameStatus.START_GAME)))
    menu = Menu(root,*a,height = 30,width = WIDTH,bg = "red")
    menu.pack(anchor = "n",pady=10,fill="x",expand=True)
    ui.pack(side="left")
    editor.pack(side="right")
    clock.pack(side = "right",fill="x",expand=True)
    popup = InputPopup("Preset of White","Insert preset code or 8 space separated piece codes, which will be saved as preset.",ui.place_preset)
    popup2 = InputPopup("Insert white piece","Insert piece code, it will be loaded into code editor.",lambda x: ui.place_piece_hash(x,3,3))

    tkinter.mainloop()