from frontend.chessboard import ChessboardUI
from frontend.popups import InputPopup, TextPopup
from frontend.menu import Menu
from frontend.chessclock import ChessClockUI
from backend.chessboard import Chessboard
from utility.constants import *
from utility.enums import colors, GameStatus
import tkinter

def start_game():
    if controller.game_status == GameStatus.NOT_STARTED:
        ui.switch_state(GameStatus.START_GAME)

def white_preset():
    InputPopup("Preset of White","Insert preset code or 8 space separated piece codes, which will be saved as preset.",lambda x:ui.place_preset(x,colors.WHITE))

def black_preset():
    InputPopup("Preset of Black","Insert preset code or 8 space separated piece codes, which will be saved as preset.",lambda x: ui.place_preset(x,colors.BLACK))

def help():
    TextPopup("Help","PRED HROU","Pomocou Place Preset ulož preset pre daného hráča. Potom klikni ľavým tlačítkom na figúrky, ktoré chceš ozačiť za kráľa.",
              "POČAS HRY","Cieľ hry: Súperovi vyprší čas alebo sa mu zníži počet kráľov.",
              "Ľavým klikom sa hýbe, pravým si vieš pozrieť, ako sa môže hýbať ľubovoľná figúrka.")

if __name__ == "__main__":
    root = tkinter.Tk()
    controller = Chessboard()
    ui = ChessboardUI(root,controller,width=WIDTH,height=HEIGHT)
    clock = ChessClockUI(root,controller,height=HEIGHT,width= 100)

    buttons = [
        ("Start Game",start_game),
        ("Place White Preset",white_preset),
        ("Place Black Preset",black_preset),
        ("Help",help),
    ]

    menu = Menu(root,*buttons,height = 30,width = WIDTH)
    menu.pack(anchor = "n",pady=10,fill="x",expand=True)
    ui.pack(side="left")
    clock.pack(side = "right",fill="x",expand=True)

    tkinter.mainloop()