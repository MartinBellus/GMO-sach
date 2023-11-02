import tkinter
from tkinter import filedialog
from frontend.chessboard import ChessboardUI


class EditorUI(tkinter.Frame):
    def __init__(self,parent : tkinter.Tk,ui : ChessboardUI,**args):
        super().__init__(parent,**args)
        self.ui = ui
        self.editor : GenomeEditor = GenomeEditor(self)
        self.file_selector : FileSelector = FileSelector(self,self.editor)
        self.place_buttom : tkinter.Button = tkinter.Button(self,text="Place piece",command=lambda : ui.place_piece(self.get_text(),4,4))
        self.place_button : PlaceButton = PlaceButton(self,self.place_piece)
        # TODO image preview? x,y input import

    def get_text(self) -> str:
        return self.editor.get("1.0","end")

    def place_piece(self,x,y,color):
        self.ui.place_piece(self.get_text(),x,y)

    def pack(self,**args):
        super().pack(fill="x",expand=True,**args)
        self.editor.pack(fill="both",expand=True)
        self.file_selector.pack(side="bottom")
        self.place_buttom.pack()
        self.place_button.pack()

        
class GenomeEditor(tkinter.Text):
    def __init__(self,parent):
        super().__init__(parent,font=("Consolas",12),width=30)

    def set_text(self,content : str):
        super().delete("1.0","end")
        super().insert("1.0",content)

class FileSelector(tkinter.Button):
    def __init__(self,parent,target : GenomeEditor):
        super().__init__(parent,text="Open Genome",command=self.select_files)
        self.target : GenomeEditor = target

    def select_files(self):
        filetypes = (
            ('Genomes', '*.dna'),
            ('All files', '*.*')
        )

        filename : str = filedialog.askopenfilename(filetypes=filetypes)

        if filename == "":
            return
        with open(filename,"r") as dna:
            content : str = ''.join(dna.readlines())
            print(repr(content))
            self.target.set_text(content)

class PlaceButton(tkinter.Frame):
    def __init__(self,parent,callback,**kwargs):
        super().__init__(parent,**kwargs)
        self.bind_all("<Return>",self.on_click)
        self.callback = callback
        self.place_button = tkinter.Button(self,text="Place piece",command=self.on_click)
        self.color_button = tkinter.Button(self,command=self.change_state,text="W",bg="white",font=("Consolas",12))
        self.form = tkinter.Entry(self,font=("Consolas",12),width=2)
        self.form.insert(0,"A1")
        self.state = 0

    def on_click(self,*args):
        try:
            x : int = int(self.form.get()[1]) - 1
            y : int = ord(self.form.get()[0].lower()) - ord('a')
            self.callback(x,y,self.state)
        except:
            self.callback(0,0,self.state)
    
    def change_state(self):
        if self.state == 0:
            self.color_button.config(text="B",bg="black",fg="white")
        else:
            self.color_button.config(text="W",bg="white",fg="black")

        self.state = (self.state+1)%2

    def pack(self,**kwargs):
        super().pack(**kwargs)
        self.form.pack(side="left",padx=5)
        self.color_button.pack(side="left")
        self.place_button.pack(side="left",padx=20)

if __name__ == "__main__":
    tk = tkinter.Tk()
    ed = EditorUI(tk)
    ed.pack(fill="both")

    tkinter.mainloop()