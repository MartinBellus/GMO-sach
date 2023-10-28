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

def invert(r : int) -> int:
    return BOARD_Y - r - 1

class ChessboardUI(tkinter.Canvas):
    squares : list[int] = [[None for _ in range(BOARD_X)] for _ in range(BOARD_Y)]
    pieces : list[int] = []
    selected : Vector = Vector(-1,-1)
    def __init__(self,root : tkinter.Tk, controller : Chessboard):
        super().__init__(root,height=HEIGHT,width=WIDTH,bg="yellow")
        self.root : tkinter.Tk = root
        self.controller : Chessboard = controller
        self.sandbox : bool =  controller.sandbox

        super().bind("<Button-1>",self.on_click)
        self.images : list[ImageTk.PhotoImage] = []
        for r in range(BOARD_Y):
            for c in range(BOARD_X):
                self.squares[invert(r)][c] = super().create_rectangle(SIZE_X*c + PADDING,    SIZE_Y*r + PADDING,
                                                                             SIZE_X*(c+1) + PADDING,SIZE_Y*(r+1) + PADDING,
                                                                             fill = Color.DEFAULT[(r+c)%2])

        for c in range(BOARD_X):
            super().create_text(SIZE_X*(c+0.5) + PADDING,HEIGHT-PADDING/2,text = str(c+1))

        for r in range(BOARD_Y):
            super().create_text(PADDING/2,SIZE_Y*(r+0.5) + PADDING,text = chr(ord('A') + invert(r)))

        self.draw_all()


    def on_click(self,event : tkinter.Event):
        click : Vector = Vector(int((event.x - PADDING)//SIZE_X),invert(int((event.y - PADDING)//SIZE_Y)))
        print(click.x,click.y)
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
            super().itemconfig(self.squares[where.y][where.x],fill=Color.MOVE[where.parity()])
            print("selecting", where.x,where.y)
    
    def do_turn(self,move : MoveDescriptor):
        super().delete("piece") # reset canvas
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
                    self.images.append(img)
                    super().create_image(PADDING + (c + 0.5)*SIZE_X,PADDING + (r + 0.5)*SIZE_Y,image=img,tag = "piece")

    def clear_selected(self,current_descriptors : list[MoveDescriptor]):
        for move in current_descriptors:
            where : Vector = move.to_position
            super().itemconfig(self.squares[where.y][where.x],fill=Color.DEFAULT[where.parity()])