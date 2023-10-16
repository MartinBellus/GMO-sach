import tkinter
from PIL import Image, ImageTk

class Color():
    DEFAULT = ["white","black"]
    SELECTED = ["gray","gray"]
    MOVE = ["blue","blue"]
    ATTACK = ["red","red"]
    SHOOT = ["green","green"]

class Move():
    NONE = 0
    MOVE = 1
    ATTACK = 2
    MOVE_AND_ATTACK = 3
    SHOOT = 4
    ATTACK_AND_MOVE = 5

COLORS = [Color.DEFAULT,Color.MOVE,Color.ATTACK,Color.SELECTED]


WIDTH = 500
HEIGHT = 500
PADDING = 30
SIZE = (WIDTH-PADDING*2)/8
DX = [ 0,-1, 0, 1] # UP, LEFT, DOWN, RIGHT
DY = [-1, 0, 1, 0]

def mozem(x,y):
    return x >= 0 and x < 8 and y >= 0 and y < 8

class Sachovnica():
    figurky = [[None for _ in range(8)] for _ in range(8)]
    policka = [[None for _ in range(8)] for _ in range(8)]
    selected = [-1,-1]
    def __init__(self,root):
        self.root = root
        self.sachovnica = tkinter.Canvas(root,height=HEIGHT,width=HEIGHT,bg="yellow")
        self.sachovnica.pack()
        self.sachovnica.bind("<Button-1>",self.on_click)
        for r in range(8):
            for c in range(8):
                self.policka[r][c] = self.sachovnica.create_rectangle(SIZE*c + PADDING,SIZE*r + PADDING,SIZE*(c+1) + PADDING,SIZE*(r+1) + PADDING,
                    fill = Color.DEFAULT[(r+c)%2])

        for c in range(8):
            self.sachovnica.create_text(SIZE*(c+0.5) + PADDING,HEIGHT-PADDING/2,text = str(c+1))

        for r in range(8):
            self.sachovnica.create_text(PADDING/2,SIZE*(r+0.5) + PADDING,text = chr(ord('A')+ 7 - r))


    def on_click(self,event):
        x = int((event.x - PADDING)//SIZE)
        y = int((event.y - PADDING)//SIZE)
        if not mozem(x,y):
            print("mimo")
            return
        if self.selected[0] == -1: #idem selectnut novu figurku
            print(x,y,self.figurky[y][x])
            if self.figurky[y][x] != None:
                self.figurky[y][x].select()
                self.selected = [y,x]
        else:
            _y,_x = self.selected

            if self.figurky[_y][_x].move(x,y): # viem sa pohnut
                pass
            elif self.selected == [y,x]: # klikam seba
                self.figurky[y][x].deselect()
                self.selected = [-1,-1]
            else:
                self.figurky[_y][_x].deselect()
                if self.figurky[y][x] != None:
                    self.figurky[y][x].select()
                    self.selected = [y,x]
                else:
                    self.selected = [-1,-1]
    def test(self):
        Pawn = Figurka(1,1,self,[2,[3,3],[1,1]],"")
        self.figurky[1][1] = Pawn
        Bishop = Figurka(3,3,self,[4,[0,5,0,0],[1,1,0,0]],"")
        self.figurky[3][3] = Bishop
        Pawn2 = Figurka(2,1,self,[2,[1,2],[1,1]],"")
        self.figurky[1][2] = Pawn2
        Divny = Figurka(5,5,self,[3,[1,1,1],[1,0,1]],"")
        self.figurky[5][5] = Divny

class Figurka:
    # x, y (indexovane zprava hore), parent object, decoded genome ([dlzka, [farby], *[moves]]), genome, image
    def __init__(self,x,y,parent,decoded_genome,genome,image = "images/Amethyst.png"): 
        self.x = x
        self.y = y
        self.dna = genome
        # decoded genome je tvaru [dlzka, [farby], .[moves]]
        self.len = decoded_genome[0]
        self.mask = decoded_genome[1]
        self.moves = decoded_genome[2:]
        self.sachovnica = parent.sachovnica
        self.parent = parent
        img = Image.open(image).resize((int(SIZE),int(SIZE)))
        self.img = ImageTk.PhotoImage(img)
        self.id = parent.sachovnica.create_image(PADDING + (x+0.5)*SIZE,PADDING + (y + 0.5)*SIZE,image=self.img)

    def generate_path(self,rotation):
        ans = [[-1 for _ in range(8)] for _ in range(8)]
        for move in self.moves:
            visited = [[[-1 for _ in range(4)] for _ in range(8)] for _ in range(8)]
            y,x = self.y, self.x
            ind = 0
            smer = rotation
            while mozem(x,y) and  visited[y][x][smer] == -1:
                print(x,y)

                # viem skocit na inu figurku
                if self.mask[ind-1] != Move.NONE and self.parent.figurky[y][x] != None and self.parent.figurky[y][x] != self:
                    # viem ju vyhodit
                    if self.mask[ind - 1] in [Move.ATTACK, Move.MOVE_AND_ATTACK]:
                        ans[y][x] = Color.ATTACK[(x + y)%2]
                    # viem vyhodit a ist dalej
                    if self.mask[ind - 1] == Move.ATTACK_AND_MOVE:
                        ans[y][x] = Color.ATTACK[(x + y)%2]
                        visited[y][x][smer] = 1
                    else:
                        break
                else:
                    # viem sa tam pohnut
                    if self.mask[ind - 1] in [Move.MOVE, Move.MOVE_AND_ATTACK, Move.ATTACK_AND_MOVE]:
                        ans[y][x] = Color.MOVE[(x + y)%2]

                    visited[y][x][smer] = 1


                # update pozicie a smeru
                y,x = y + DY[smer]*move[ind],x + DX[smer]*move[ind]
                smer = (smer + 1)%4
                ind = (ind + 1)%self.len
                print("->",x,y)

        ans[self.y][self.x] = Color.DEFAULT[(self.y + self.x)%2] 
        return ans


    # ofarbenie policok, kam sa  viem dostat
    def select(self):
        for smer in range(4):
            pattern = self.generate_path(smer)
            for i in pattern:
                print(*i)
            for r in range(8):
                for c in range(8):
                    if pattern[r][c] != -1:
                        self.sachovnica.itemconfig(self.parent.policka[r][c],fill=pattern[r][c])


    # pohne figurku na x,y (ak sa da) a vrati ci sa da
    def move(self,x,y):
        return 0

    # reset vsetkych policok
    def deselect(self):
        for r in range(8):
            for c in range(8):
                self.sachovnica.itemconfig(self.parent.policka[r][c],fill=Color.DEFAULT[(r+c)%2])



root = tkinter.Tk()

sachovnica = Sachovnica(root)

sachovnica.test()

tkinter.mainloop()