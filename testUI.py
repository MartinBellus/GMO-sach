from frontend.chessboard import ChessboardUI
from frontend.genome_editor import EditorUI
from frontend.popups import PopupWindow
from frontend.menu import Menu
from backend.chessboard import Chessboard
from utility.constants import *
from utility.enums import colors
import tkinter

def nic():
    print("nic")

if __name__ == "__main__":
    root = tkinter.Tk()
    cnt = Chessboard(0)
    ui = ChessboardUI(root,cnt,width=WIDTH,height=HEIGHT,bg="yellow")
    editor = EditorUI(root,ui,width=100,height=HEIGHT,bg="green")
    a = [(f"test{i}",nic) for i in range(5)]
    a.append(("Start Game",ui.switch_state(1)))
    menu = Menu(root,*a,height = 30,width = WIDTH,bg = "red")
    menu.pack(anchor = "n",pady=10,fill="x",expand=True)
    ui.pack(side="left")
    editor.pack(side="right")
    popup = PopupWindow("Preset of White","Insert preset code or 8 space separated piece codes, which will be saved as preset.",ui.place_preset)
    popup2 = PopupWindow("Insert white piece","Insert piece code, it will be loaded into code editor.",lambda x: ui.place_piece_hash(x,3,3))

    tkinter.mainloop()