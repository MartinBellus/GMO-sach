import tkinter

class Menu(tkinter.Frame):
    """
    Class for menu buttons

    Args:
        parent : parent widget
        args : list of tuples with button text and command
        kwargs : keywords for tkinter.Frame
    """
    def __init__(self,parent,*buttons,**kwargs):
        super().__init__(parent,**kwargs)
        self.buttons = [
            tkinter.Button(self,text = b[0],command = b[1]) for b in buttons
        ]

    def pack(self,**kwargs):
        super().pack(**kwargs)
        for b in self.buttons:
            b.pack(anchor="w",side = "left",padx=5)
