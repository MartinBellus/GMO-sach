from frontend.chessboard import ChessboardUI
from frontend.genome_editor import EditorUI
from frontend.popups import PopupWindow
from backend.chessboard import Chessboard
from utility.constants import *
from utility.enums import colors
import tkinter

if __name__ == "__main__":
    root = tkinter.Tk()
    cnt = Chessboard(1)
    ui = ChessboardUI(root,cnt)
    editor = EditorUI(root,ui,width=200,height=HEIGHT)
    ui.pack(side="left")
    editor.pack(side="right")
    popup = PopupWindow("Preset of White","Insert preset code or 8 space separated piece codes, which will be saved as preset.",ui.place_preset)
    popup2 = PopupWindow("Insert white piece","Insert piece code, it will be loaded into code editor.",lambda x: ui.place_piece_hash(x,3,3))

    tkinter.mainloop()