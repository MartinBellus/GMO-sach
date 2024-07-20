import tkinter
from backend.chessboard import Chessboard
from utility.enums import colors

class ChessClockUI(tkinter.Frame):
    """
    Class that displays remaining time for both players

    Args:
        parent : parent widget
        controller : chessboard controller
        kwargs : keywords for tkinter.Frame
    """
    def __init__(self,parent,controller : Chessboard,**kwargs):
        super().__init__(parent,**kwargs)
        self.controller = controller
        self.white_time = tkinter.Label(self,font=("Consolas",20))
        self.black_time = tkinter.Label(self,font=("Consolas",20))
        self.update()

    def update(self):
        """
        Fetch remaining time from controller and update labels.
        Runs every 500ms
        """
        white_time_left = int(self.controller.get_remaining_time(colors.WHITE))
        black_time_left = int(self.controller.get_remaining_time(colors.BLACK))
        self.white_time.config(text=f"{white_time_left//60:02}:{white_time_left%60:02}")
        self.black_time.config(text=f"{black_time_left//60:02}:{black_time_left%60:02}")
        if self.controller.get_current_player() == colors.WHITE:
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