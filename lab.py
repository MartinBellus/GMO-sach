from frontend.chessboard import ChessboardUI
from frontend.genome_editor import EditorUI
from frontend.popups import InputPopup,TextPopup
from frontend.menu import Menu
from backend.chessboard import Chessboard
from backend.genome import Genome
from utility.constants import *
from utility.enums import colors
import tkinter


def help():
    # TODO
    TextPopup("Help","glupy si")

def white_preset():
    InputPopup("Preset of White","Insert preset code or 8 space separated piece codes, which will be saved as preset.",lambda x:ui.place_preset(x,colors.WHITE))

def black_preset():
    InputPopup("Preset of Black","Insert preset code or 8 space separated piece codes, which will be saved as preset.",lambda x: ui.place_preset(x,colors.BLACK))

def save_as():
    InputPopup("Save piece as","Path to file, where you want to save piece",lambda x:editor.save_to(x))
 
def fetch():
    InputPopup("Fetch piece from key","Insert piece code, it will be loaded into code editor.",lambda x: editor.editor.set_text(Genome.from_hash(x).raw_dna))

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("LAB")
    controller = Chessboard(1)
    ui = ChessboardUI(root,controller,width=WIDTH,height=HEIGHT)
    editor = EditorUI(root,ui,width=100,height=HEIGHT)

    buttons = [
        ("Reset",lambda : ui.reset()),
        ("Place white preset",white_preset),
        ("Place black preset",black_preset),
        ("Save piece",save_as),
        ("Fetch piece",fetch),
        ("Help",help),
    ]

    menu = Menu(root,*buttons,height = 30,width = WIDTH)
    menu.pack(anchor = "n",pady=10,fill="x",expand=True)
    ui.pack(side="left")
    editor.pack(side="right")
    tkinter.mainloop()