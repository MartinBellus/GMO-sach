import tkinter

class Menu(tkinter.Frame):
    def __init__(self,parent,*args,**kwargs):
        super().__init__(parent,**kwargs)
        self.buttons = [
            tkinter.Button(self,text = b[0],command = b[1]) for b in args
        ]
    def pack(self,**kwargs):
        super().pack(**kwargs)
        for b in self.buttons:
            b.pack(anchor="w",side = "left",padx=5)