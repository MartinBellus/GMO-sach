import tkinter
from PIL import Image, ImageTk
from frontend.popups import TextPopup
from frontend.image_selector import ImageSelector
from backend.chessboard import Chessboard, PieceInfo
from backend.move_descriptor import MoveDescriptor
from backend.genome import Genome
from backend.piece import Piece
from backend.preset import Preset
from utility.constants import *
from utility.vector import Vector, inside_chessboard 
from utility.enums import colors, GameStatus

class Color:
    #           BIELE       CIERNE
    DEFAULT =   ["#eae9d2"  ,"#4b7399"]
    SELECTED =  ["gray"     ,"gray"]
    MOVE =      ["#b7d171"  ,"#87a65a"]
    ATTACK =    ["#eb7b6a"  ,"#cb645e"]
    SHOOT =     ["green"    ,"green"]

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
        self.selector : ImageSelector = ImageSelector(int(self.size_x),int(self.size_y))

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
            self.switch_state(GameStatus.LAB)
        else:
            self.switch_state(GameStatus.NOT_STARTED)

    def switch_state(self,new_state : GameStatus,*args):
        super().delete("text")
        match new_state:
            case GameStatus.NOT_STARTED:
                # load preset alebo nahadzat figurky
                super().create_text(self.width/2,PADDING/2,text="Please select piece presets.",anchor="center",justify="center",tag="text")
            case GameStatus.START_GAME:
                # zacne hru
                self.controller.start_game()
                super().create_text(self.width/2,PADDING/2,text="Game will start soon.",anchor="center",justify="center",tag="text")
                self.bind("<Button-1>",self.ingame_click)
                self.redraw_pieces()
                self.switch_state(GameStatus.IN_PROGRESS)
            case GameStatus.IN_PROGRESS:
                if self.controller.get_current_player() == colors.WHITE:
                    super().create_text(self.width/2,PADDING/2,text="White turn.",anchor="center",justify="center",tag="text")
                else:
                    super().create_text(self.width/2,PADDING/2,text="Black turn.",anchor="center",justify="center",tag="text")
            case GameStatus.WHITE_WON:
                print("game over")
                super().create_text(self.width/2,PADDING/2,text="!!! WHITE WON !!!",anchor="center",justify="center",tag="text")
                self.bind("<Button-1>",lambda x: self.switch_state(GameStatus.PRE_GAME))
            case GameStatus.BLACK_WON:
                print("game over")
                super().create_text(self.width/2,PADDING/2,text="!!! BLACK WON !!!",anchor="center",justify="center",tag="text")
                self.bind("<Button-1>",lambda x: self.switch_state(GameStatus.PRE_GAME))
            case GameStatus.DRAW:
                print("game over")
                super().create_text(self.width/2,PADDING/2,text="DRAW",anchor="center",justify="center",tag="text")
                self.bind("<Button-1>",lambda x: self.switch_state(GameStatus.PRE_GAME))
            case GameStatus.LAB:
                super().create_text(self.width/2,PADDING/2,text="Welcome to LAB",anchor="center",justify="center",tag="text")
                self.bind("<Button-1>",self.ingame_click)
                self.bind("<Button-3>",self.get_dna)
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

    def get_dna(self,event : tkinter.Event):
        click : Vector = Vector(int((event.x - PADDING)//self.size_x),invert(int((event.y - PADDING)//self.size_y)))
        if not inside_chessboard(click):
            return
        if click in self.controller.chessboard:
            TextPopup("Piece Info",repr(self.controller.chessboard[click]))

    def draw_moves(self,current_descriptors : list[MoveDescriptor]):
        for move in current_descriptors:
            where : Vector = move.to_position
            super().itemconfig(self.squares[where.y][where.x],fill=Color.MOVE[where.parity()])
            print("selecting", where.x,where.y)
    
    def do_turn(self,move : MoveDescriptor):
        gameState : GameStatus = self.controller.do_move(move)
        self.redraw_pieces()
        self.switch_state(gameState)

    def redraw_pieces(self):
        super().delete("piece") # reset canvas
        state : list[list[None | PieceInfo]] = self.controller.get_board_for_reading()
        for r in range(BOARD_Y):
            for c in range(BOARD_X):
                if state[invert(r)][c] != None:
                    # nakresli na dane policko figurku
                    # TODO image selector
                    img = self.selector.get_image(state[invert(r)][c])
                    self.images.append(img)
                    super().create_image(PADDING + (c + 0.5)*self.size_x,PADDING + (r + 0.5)*self.size_y,image=img,tag = "piece")

    def clear_selected(self,current_descriptors : list[MoveDescriptor]):
        for move in current_descriptors:
            where : Vector = move.to_position
            super().itemconfig(self.squares[where.y][where.x],fill=Color.DEFAULT[where.parity()])

    def place_piece(self, dna : str,color : colors, x : int, y : int):
        self.controller.insert_piece_by_dna(dna,color,Vector(x,y),False,True)
        self.redraw_pieces()

    def place_piece_hash(self,hash : str, color: colors, x : int, y : int):
        try:
            self.controller.insert_piece(hash,color,Vector(x,y),False,True)
        except Exception as ex:
            raise ex
        self.redraw_pieces()

    def place_preset(self, preset : str,color : colors):
        parsed_preset : list(str) = preset.strip().split()
        try:
            if len(parsed_preset) == 1:
                self.controller.load_preset(Preset.fetch_preset(parsed_preset[0]),color)
            else:
                self.controller.load_preset(Preset(parsed_preset),color)
            self.redraw_pieces()
        except Exception as ex:
            raise ex

    def reset(self):
        while len(self.controller.chessboard):
            self.controller.erase_piece(list(self.controller.chessboard.keys())[0])
        self.redraw_pieces()