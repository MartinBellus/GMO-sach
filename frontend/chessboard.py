import tkinter
from PIL import Image, ImageTk
from backend.chessboard import Chessboard, PieceInfo
from backend.move_descriptor import MoveDescriptor
from utility.constants import *
from utility.vector import Vector, inside_chessboard 
from utility.enums import *

class Color():
    #           BIELE       CIERNE
    DEFAULT =   ["#eae9d2"  ,"#4b7399"]
    SELECTED =  ["gray"     ,"gray"]
    MOVE =      ["#b7d171"  ,"#87a65a"]
    ATTACK =    ["#eb7b6a"  ,"#cb645e"]
    SHOOT =     ["green"    ,"green"]

class ChessboardUI:
    squares : list[int] = [[None for _ in range(BOARD_X)] for _ in range(BOARD_Y)]
    pieces : list[int] = []
    selected : Vector = Vector(-1,-1)
    def __init__(self,root : tkinter.Tk, sandbox : bool = 0):
        self.root : tkinter.Tk = root
        self.controller : Chessboard = Chessboard(sandbox)

        self.chessboard_canvas = tkinter.Canvas(root,height=HEIGHT,width=HEIGHT,bg="yellow")
        self.chessboard_canvas.pack()
        self.chessboard_canvas.bind("<Button-1>",self.on_click)
        self.chessboard_canvas.images : list[ImageTk.PhotoImage]= []
        for r in range(BOARD_Y):
            for c in range(BOARD_X):
                self.squares[r][c] = self.chessboard_canvas.create_rectangle(SIZE_X*c + PADDING,    SIZE_Y*r + PADDING,
                                                                             SIZE_X*(c+1) + PADDING,SIZE_Y*(r+1) + PADDING,
                                                                             fill = Color.DEFAULT[(r+c)%2])

        for c in range(BOARD_X):
            self.chessboard_canvas.create_text(SIZE_X*(c+0.5) + PADDING,HEIGHT-PADDING/2,text = str(c+1))

        for r in range(BOARD_Y):
            self.chessboard_canvas.create_text(PADDING/2,SIZE_Y*(r+0.5) + PADDING,text = chr(ord('A')+ 7 - r))

        if __name__ == "__main__":
            self.controller._insert_piece(Piece(Genome(PAWN_DNA),colors.BLACK,1),Vector(0,0))
            self.controller._insert_piece(Piece(Genome(PAWN_DNA),colors.BLACK,1),Vector(1,1))
            self.controller._insert_piece(Piece(Genome(PAWN_DNA),colors.WHITE,1),Vector(2,2))

        self.draw_all()


    def on_click(self,event : tkinter.Event):
        click : Vector = Vector(int((event.x - PADDING)//SIZE_X),int((event.y - PADDING)//SIZE_Y))
        if not inside_chessboard(click):
            print("mimo")
            return
        current_descriptors : list[MoveDescriptor] = self.controller.get_moves(self.selected)
        self.clear_selected(current_descriptors)

        if self.selected == click: # klikol som znova na seba
            print("klik na seba")
            self.selected = Vector(-1,-1)
        else:
            for move in current_descriptors:
                if move.to_position == click: # viem sa pohnut
                    print("hybem sa dakam")
                    self.do_turn(move)
                    self.selected = Vector(-1,-1)
                    return
            else: # klikol som dakam, kam neviem ist
                print("nikam sa nehybem, novy selected")
                self.selected = click
            self.draw_moves(self.controller.get_moves(click))

    def draw_moves(self,current_descriptors : list[MoveDescriptor]):
        for move in current_descriptors:
            where : Vector = move.to_position
            self.chessboard_canvas.itemconfig(self.squares[where.y][where.x],fill=Color.MOVE[where.parity()])
            print("selecting", where.x,where.y)
    
    def do_turn(self,move : MoveDescriptor):
        self.chessboard_canvas.delete("piece") # reset canvas
        gameState : GameStatus = self.controller.do_move(move)
        self.draw_all()

    def draw_all(self):
        state : list[list[None | PieceInfo]] = self.controller.get_board_for_reading()
        for r in range(BOARD_Y):
            for c in range(BOARD_X):
                if state[r][c] != None:
                    # nakresli na dane policko figurku
                    # TODO image selector
                    if state[r][c].color == colors.WHITE:
                        image : str = "images/Bar_of_Soap.png"
                    else:
                        image : str = "images/Anchor.png"
                    img = ImageTk.PhotoImage(Image.open(image).resize((int(SIZE_X),int(SIZE_Y))))
                    self.chessboard_canvas.images.append(img)
                    self.chessboard_canvas.create_image(PADDING + (c + 0.5)*SIZE_X,PADDING + (r + 0.5)*SIZE_Y,image=img,tag = "piece")

    def clear_selected(self,current_descriptors : list[MoveDescriptor]):
        for move in current_descriptors:
            where : Vector = move.to_position
            self.chessboard_canvas.itemconfig(self.squares[where.y][where.x],fill=Color.DEFAULT[where.parity()])


if __name__ == "__main__":
    # for testing
    from backend.piece import Piece
    from backend.genome import Genome
    root = tkinter.Tk()

    sachovnica = ChessboardUI(root,1)
    sachovnica2 = ChessboardUI(root,0)

    tkinter.mainloop()