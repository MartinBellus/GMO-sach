from frontend.chessboard import ChessboardUI
from frontend.genome_editor import EditorUI
from backend.chessboard import Chessboard
import tkinter

if __name__ == "__main__":
    root = tkinter.Tk()
    cnt = Chessboard(0)
    ui = ChessboardUI(root,cnt)
    editor = EditorUI(root,width=200)
    ui.pack(side="left")
    editor.pack(side="right")

    tkinter.mainloop()