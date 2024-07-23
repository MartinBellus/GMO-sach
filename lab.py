from frontend.chessboard import ChessboardUI
from frontend.genome_editor import EditorUI
from frontend.popups import InputPopup,TextPopup
from frontend.menu import Menu
from backend.chessboard import Chessboard
from backend.genome import Genome
from backend.preset import Preset
from utility.constants import *
from utility.enums import Colors
import tkinter


def help():
    # TODO
    TextPopup("Help","Ľavým klikom sa pohybujú figúrky, pravým zistíš, aký má daná figúrka kód.",
              "Napravo sa nachádza editor, v ktorom môžeš meniť genóm figúrky a vkladať ju na plochu. Pomocou Fetch Piece alebo Open Genome môžeš načítať už existujúci genóm do editora.",
              "Pomocou Save Preset si môžeš uložiť aktuálne rozloženie figúrok pre bieleho a čierneho hráča.", ttl=10000)

def white_preset():
    InputPopup("Preset of White","Insert preset code or 8 space separated piece codes, which will be saved as preset.",
        lambda x:ui.place_preset(x,Colors.WHITE))

def black_preset():
    InputPopup("Preset of Black","Insert preset code or 8 space separated piece codes, which will be saved as preset.",
        lambda x: ui.place_preset(x,Colors.BLACK))

def save_preset():
    board = controller.get_board_for_reading()
    hashes_top : list[str] = []
    hashes_bot : list[str] = []
    for i in range(BOARD_X):
        if board[-1][i] != None:
            hashes_top.append(board[-1][i].genome_hash)
        if board[0][i] != None:
            hashes_bot.append(board[0][i].genome_hash)
    if len(hashes_top) == BOARD_X:
        preset_top : Preset = Preset(hashes_top)
        TextPopup("Black Preset Key",f"Black preset pieces: {hashes_top}",
            f"Black preset key: {preset_top.hash()}", ttl=10000)
    if len(hashes_bot) == BOARD_X:
        preset_bot : Preset = Preset(hashes_bot)
        TextPopup("White Preset Key",f"White preset pieces: {hashes_bot}",
            f"White preset key: {preset_bot.hash()}", ttl=10000)
    if len(hashes_bot) != BOARD_X and len(hashes_top) != BOARD_X:
        TextPopup("Error",f"Place {BOARD_X} pieces in bottom or top row.")

def save_as():
    InputPopup("Save piece as","Path to file, where you want to save piece",
        lambda x:editor.save_to(x))

def fetch():
    InputPopup("Fetch piece from key","Insert piece code, it will be loaded into code editor.",
        lambda x: editor.editor.set_text(Genome.from_hash(x).raw_dna))

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("LAB")
    controller = Chessboard(True)
    ui = ChessboardUI(root,controller,width=WIDTH,height=HEIGHT)
    editor = EditorUI(root,ui,width=100,height=HEIGHT)

    buttons = [
        ("Reset",lambda : ui.reset()),
        ("Place White Preset",white_preset),
        ("Place Black Preset",black_preset),
        ("Save Piece",save_as),
        ("Save Preset",save_preset),
        ("Fetch Piece",fetch),
        ("Help",help),
    ]

    menu = Menu(root,*buttons,height = 30,width = WIDTH)
    menu.pack(anchor = "n",pady=10,fill="x",expand=True)
    ui.pack(side="left")
    editor.pack(side="right")
    tkinter.mainloop()
