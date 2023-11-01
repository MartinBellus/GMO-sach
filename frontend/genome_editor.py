import tkinter
from tkinter import filedialog
from frontend.chessboard import ChessboardUI


class EditorUI(tkinter.Frame):
    def __init__(self,parent : tkinter.Tk,ui : ChessboardUI,**args):
        super().__init__(parent,**args)
        self.editor : GenomeEditor = GenomeEditor(self)
        self.file_selector : FileSelector = FileSelector(self,self.editor)
        self.place_buttom : tkinter.Button = tkinter.Button(self,text="Place piece",command=lambda : ui.place_piece(self.get_text(),4,4))
        # TODO image preview? x,y input import

    def get_text(self) -> str:
        return self.editor.get("1.0","end")

    def pack(self,**args):
        super().pack(fill="x",expand=True,**args)
        super().pack_propagate(False)
        self.editor.pack(fill="both",expand=True)
        self.file_selector.pack(side="bottom")
        self.place_buttom.pack()
        
class GenomeEditor(tkinter.Text):
    def __init__(self,parent):
        super().__init__(parent,font=("Consolas",12))

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

if __name__ == "__main__":
    tk = tkinter.Tk()
    ed = EditorUI(tk)
    ed.pack(fill="both")

    tkinter.mainloop()