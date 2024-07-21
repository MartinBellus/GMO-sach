import tkinter
from tkinter import filedialog
from frontend.chessboard import ChessboardUI
from utility.enums import Colors


class EditorUI(tkinter.Frame):
    """
    Component for editing genomes. Contains text editor, file selector and place button

    Args:
        parent : parent widget
        ui : chessboard ui
        kwargs : keywords for tkinter.Frame
    """
    def __init__(self,parent : tkinter.Tk,ui : ChessboardUI,**args):
        super().__init__(parent,**args)
        self.ui = ui
        self.editor : GenomeEditor = GenomeEditor(self)
        self.file_selector : FileSelector = FileSelector(self,self.editor)
        self.place_button : PlaceButton = PlaceButton(self,self.place_piece)

    def get_text(self) -> str:
        return self.editor.get("1.0","end")

    def place_piece(self,color : Colors,x,y):
        """
        Place piece with current genome at specified position

        Args:
            color : color of piece
            x : x coordinate
            y : y coordinate
        """
        self.ui.place_piece(self.get_text(),color,x,y)
    
    def save_to(self,name : str):
        """
        Save current genome to file

        Args:
            name : file name 
        """
        try:
            with open(name,"w") as file:
                file.write(self.get_text())
        except Exception as ex:
            raise ex


    def pack(self,**args):
        super().pack(fill="x",expand=True,**args)
        self.editor.pack(fill="both",expand=True)
        self.file_selector.pack(side="bottom")
        self.place_button.pack(pady=5)

        
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
        """
        Open file dialog and load genome from file
        """
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
        self.callback = callback
        self.place_button = tkinter.Button(self,text="Place piece",command=self.on_click)
        self.color_button = tkinter.Button(self,command=self.change_state,text="W",bg="white",font=("Consolas",12))
        self.form = tkinter.Entry(self,font=("Consolas",12),width=2)
        self.form.insert(0,"A1")
        self.state : Colors = Colors.WHITE 

    def on_click(self,*args):
        try:
            x : int = int(self.form.get()[1]) - 1
            y : int = ord(self.form.get()[0].lower()) - ord('a')
            self.callback(self.state,x,y)
        except:
            self.callback(self.state,0,0)
    
    def change_state(self):
        if self.state == Colors.WHITE:
            self.color_button.config(text="B",bg="black",fg="white")
            self.state = Colors.BLACK
        else:
            self.color_button.config(text="W",bg="white",fg="black")
            self.state = Colors.WHITE

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