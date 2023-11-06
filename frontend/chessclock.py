import tkinter
from backend.chessboard import Chessboard
from utility.enums import colors

class ChessClockUI(tkinter.Frame):
    def __init__(self,parent,controller : Chessboard,**kwargs):
        super().__init__(parent,**kwargs)
        self.controller = controller
        self.white_time = tkinter.Label(self,font=("Consolas",20))
        self.black_time = tkinter.Label(self,font=("Consolas",20))
        self.update()

    def update(self):
        print("update")
        self.white_time.config(text=f"{self.controller.get_remaining_time(colors.WHITE)}")
        self.black_time.config(text=f"{self.controller.get_remaining_time(colors.BLACK)}")
        if self.controller.get_current_player == colors.WHITE:
            self.white_time.config(font=("Consolas",20,"bold"))
            self.black_time.config(font=("Consolas",20))
        else:
            self.white_time.config(font=("Consolas",20))
            self.black_time.config(font=("Consolas",20,"bold"))
        self.after(500,self.update)
    def pack(self,**kwargs):
        super().pack(**kwargs)
        self.black_time.pack(padx=15)
        self.white_time.pack(padx=15)