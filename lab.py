from frontend.chessboard import ChessboardUI
from frontend.genome_editor import EditorUI
from frontend.popups import InputPopup, TextPopup
from frontend.menu import Menu
from backend.chessboard import Chessboard
from backend.genome_cache import fetch_dna
from utility.constants import *
from utility.enums import Colors
import tkinter


def help():
    TextPopup("Help", "Ľavým klikom sa pohybujú figúrky, pravým zistíš, aký má daná figúrka kód.",
              "Napravo sa nachádza editor, v ktorom môžeš meniť genóm figúrky a vkladať ju na plochu. Pomocou Fetch Piece alebo Open Genome môžeš načítať už existujúci genóm do editora.",
              "Pomocou Save Preset si môžeš uložiť aktuálne rozloženie figúrok pre bieleho a čierneho hráča.", ttl=10000)


def white_preset():
    InputPopup("Preset of White", "Insert preset code to be placed for white player.",
               lambda x: ui.place_preset(x, Colors.WHITE))


def black_preset():
    InputPopup("Preset of Black", "Insert preset code to be placed for black player.",
               lambda x: ui.place_preset(x, Colors.BLACK))


def save_preset():
    preset_top = controller.save_preset(Colors.BLACK)
    preset_bot = controller.save_preset(Colors.WHITE)
    if preset_top != None:
        TextPopup("Black Preset Key", f"Black preset saved with key: {
                  preset_top}", ttl=10000)
    if preset_bot != None:
        TextPopup("White Preset Key", f"White preset saved with key: {
                  preset_bot}", ttl=10000)
    if preset_bot == None and preset_top == None:
        TextPopup("Error", f"Place {BOARD_X} pieces in bottom or top row.")


def save_as():
    InputPopup("Save piece as", "Path to file, where you want to save piece",
               lambda x: editor.save_to(x))


def fetch():
    InputPopup("Fetch piece from key", "Insert piece code, it will be loaded into code editor.",
               lambda x: editor.editor.set_text(fetch_dna(x)))


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("LAB")
    controller = Chessboard(True)
    ui = ChessboardUI(root, controller, width=WIDTH, height=HEIGHT)
    editor = EditorUI(root, ui, width=100, height=HEIGHT)

    buttons = [
        ("Reset", lambda: ui.reset()),
        ("Place White Preset", white_preset),
        ("Place Black Preset", black_preset),
        ("Save Piece", save_as),
        ("Save Preset", save_preset),
        ("Fetch Piece", fetch),
        ("Help", help),
    ]

    menu = Menu(root, *buttons, height=30, width=WIDTH)
    menu.pack(anchor="n", pady=10, fill="x", expand=True)
    ui.pack(side="left")
    editor.pack(side="right")
    tkinter.mainloop()
