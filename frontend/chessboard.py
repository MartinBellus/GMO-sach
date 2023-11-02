import tkinter
from PIL import Image, ImageTk
from backend.chessboard import Chessboard, PieceInfo
from backend.move_descriptor import MoveDescriptor
from backend.genome import Genome
from backend.piece import Piece
from backend.preset import Preset
from utility.constants import *
from utility.vector import Vector, inside_chessboard 
from utility.enums import *

class Color:
    #           BIELE       CIERNE
    DEFAULT =   ["#eae9d2"  ,"#4b7399"]
    SELECTED =  ["gray"     ,"gray"]
    MOVE =      ["#b7d171"  ,"#87a65a"]
    ATTACK =    ["#eb7b6a"  ,"#cb645e"]
    SHOOT =     ["green"    ,"green"]

class State:
    PRE_GAME    = 0
    GAME_START  = 1
    WHITE_TURN  = 2 
    BLACK_TURN  = 3
    PROMOTE     = 4
    GAME_OVER   = 5
    LAB         = 6

def invert(r : int) -> int:
    return BOARD_Y - r - 1

PADDING = 30

class ChessboardUI(tkinter.Canvas):

    squares : list[int] = [[None for _ in range(BOARD_X)] for _ in range(BOARD_Y)]
    selected : Vector = Vector(-1,-1)
    images : list[ImageTk.PhotoImage] = []

    def __init__(self,root : tkinter.Tk, controller : Chessboard,width = WIDTH,height = HEIGHT,**kwargs):
        super().__init__(root,width=width,height=height,**kwargs)
        self.root : tkinter.Tk = root
        self.controller : Chessboard = controller

        self.size_x = (width - PADDING*2)/BOARD_X
        self.size_y = (height - PADDING*2)/BOARD_Y
        self.height = height
        self.width = width

        for r in range(BOARD_Y):
            for c in range(BOARD_X):
                self.squares[invert(r)][c] = super().create_rectangle(self.size_x*c + PADDING,    self.size_y*r + PADDING,
                                                                             self.size_x*(c+1) + PADDING,self.size_y*(r+1) + PADDING,
                                                                             fill = Color.DEFAULT[(invert(r)+c)%2])

        for c in range(BOARD_X):
            super().create_text(self.size_x*(c+0.5) + PADDING,self.height-PADDING/2,text = str(c+1))

        for r in range(BOARD_Y):
            super().create_text(PADDING/2,self.size_y*(r+0.5) + PADDING,text = chr(ord('A') + invert(r)))

        if controller.sandbox:
            self.switch_state(State.LAB)
        else:
            self.switch_state(State.PRE_GAME)

    def switch_state(self,new_state : int,*args):
        super().delete("text")
        match new_state:
            case State.PRE_GAME:
                # load preset alebo nahadzat figurky
                super().create_text(self.width/2,PADDING/2,text="Please select piece presets.",anchor="center",justify="center",tag="text")
            case State.GAME_START:
                # zacne hru
                super().create_text(self.width/2,PADDING/2,text="Game will start soon.",anchor="center",justify="center",tag="text")
                self.bind("<Button-1>",self.ingame_click)
                self.redraw_pieces()
                self.switch_state(State.WHITE_TURN)
            case State.WHITE_TURN:
                super().create_text(self.width/2,PADDING/2,text="White turn.",anchor="center",justify="center",tag="text")
            case State.BLACK_TURN:
                super().create_text(self.width/2,PADDING/2,text="Black turn.",anchor="center",justify="center",tag="text")
            case State.PROMOTE:
                super().create_text(self.width/2,PADDING/2,text="Black turn.",anchor="center",justify="center",tag="text")
            case State.GAME_OVER:
                print("game over")
                super().create_text(self.width/2,PADDING/2,text=args[0],anchor="center",justify="center",tag="text")
                self.bind("<Button-1>",lambda x: self.switch_state(State.PRE_GAME))
            case State.LAB:
                super().create_text(self.width/2,PADDING/2,text="Welcome to LAB",anchor="center",justify="center",tag="text")
                self.bind("<Button-1>",self.ingame_click)
                self.redraw_pieces()
            case _:
                print("neexistuje")
                raise Exception("Game state does not exist")

    def ingame_click(self,event : tkinter.Event):
        click : Vector = Vector(int((event.x - PADDING)//self.size_x),invert(int((event.y - PADDING)//self.size_y)))
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
        gameState : GameStatus = self.controller.do_move(move)
        self.redraw_pieces()
        match gameState:
            case GameStatus.WHITE_WON:
                self.switch_state(State.GAME_OVER,"!!! WHITE WON !!!")
            case GameStatus.BLACK_WON:
                self.switch_state(State.GAME_OVER,"!!! BLACK WON !!!")
            case GameStatus.DRAW:
                self.switch_state(State.GAME_OVER,"DRAW")
            case GameStatus.PROMOTION_POSSIBLE:
                # TODO promoting
                ...
            case GameStatus.IN_PROGRESS:
                self.switch_state(State.BLACK_TURN if self.controller.get_current_player == colors.BLACK else State.WHITE_TURN)
            case _:
                raise Exception("Wrong game status")

    def redraw_pieces(self):
        super().delete("piece") # reset canvas
        state : list[list[None | PieceInfo]] = self.controller.get_board_for_reading()
        for r in range(BOARD_Y):
            for c in range(BOARD_X):
                if state[invert(r)][c] != None:
                    # nakresli na dane policko figurku
                    # TODO image selector
                    if state[invert(r)][c].color == colors.WHITE:
                        image : str = "images/Bar_of_Soap.png"
                    else:
                        image : str = "images/Anchor.png"
                    img = ImageTk.PhotoImage(Image.open(image).resize((int(self.size_x),int(self.size_y))))
                    self.images.append(img)
                    super().create_image(PADDING + (c + 0.5)*self.size_x,PADDING + (r + 0.5)*self.size_y,image=img,tag = "piece")

    def clear_selected(self,current_descriptors : list[MoveDescriptor]):
        for move in current_descriptors:
            where : Vector = move.to_position
            super().itemconfig(self.squares[where.y][where.x],fill=Color.DEFAULT[where.parity()])

    def place_piece(self, dna : str, x : int, y : int):
        self.controller._insert_piece(Piece(Genome(dna),colors.BLACK),Vector(x,y))
        self.redraw_pieces()

    def place_piece_hash(self,hash : str, x : int, y : int):
        try:
            self.controller.insert_piece(hash,colors.WHITE,Vector(x,y))
        except Exception as ex:
            raise ex
        self.redraw_pieces()

    def place_preset(self, preset : str):
        parsed_preset : list(str) = preset.strip().split()
        try:
            if len(parsed_preset) == 1:
                self.controller.load_preset(Preset.fetch_preset(parsed_preset[0]),colors.WHITE)
            else:
                self.controller.load_preset(Preset(parsed_preset),colors.WHITE)
            self.redraw_pieces()
        except Exception as ex:
            raise ex