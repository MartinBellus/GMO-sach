import tkinter
from PIL import Image, ImageTk

class Color():
    #           BIELE       CIERNE
    DEFAULT =   ["#eae9d2"  ,"#4b7399"]
    SELECTED =  ["gray"     ,"gray"]
    MOVE =      ["#b7d171"  ,"#87a65a"]
    ATTACK =    ["#eb7b6a"  ,"#cb645e"]
    SHOOT =     ["green"    ,"green"]

class Move():
    NONE = 0
    MOVE = 1
    ATTACK = 2
    MOVE_AND_ATTACK = 3
    SHOOT = 4
    ATTACK_AND_MOVE = 5

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
                self.selected = [-1,-1]
                self.figurky[y][x].deselect()
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
        Divny = Figurka(5,5,self,[2,[0,3],[2,1],[1,2]],"")
        self.figurky[5][5] = Divny
        # TODO shoot nefunguje
        Dama = Figurka(7,7,self,[4,[0,4,0,0],[0,1,0,0],[1,1,0,0]],"")
        self.figurky[7][7] = Dama

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
            while mozem(x,y) and visited[y][x][smer] == -1:
                # viem skocit na inu figurku
                if self.mask[ind-1] != Move.NONE and self.parent.figurky[y][x] != None and self.parent.figurky[y][x] != self:
                    # viem ju vyhodit
                    if self.mask[ind - 1] in [Move.ATTACK, Move.MOVE_AND_ATTACK]:
                        ans[y][x] = Move.ATTACK
                    # viem ju zastrelit
                    if self.mask[ind - 1] == Move.SHOOT:
                        ans[y][x] = Move.SHOOT
                    # viem vyhodit a ist dalej
                    if self.mask[ind - 1] == Move.ATTACK_AND_MOVE:
                        ans[y][x] = Move.ATTACK
                        visited[y][x][smer] = 1
                    else:
                        break
                else:
                    # viem sa tam pohnut
                    if self.mask[ind - 1] in [Move.MOVE, Move.MOVE_AND_ATTACK, Move.ATTACK_AND_MOVE, Move.SHOOT]:
                        ans[y][x] = Move.MOVE

                    visited[y][x][smer] = 1


                # update pozicie a smeru
                y,x = y + DY[smer]*move[ind],x + DX[smer]*move[ind]
                smer = (smer + 1)%4
                ind = (ind + 1)%self.len

        return ans


    # ofarbenie policok, kam sa  viem dostat
    def select(self):
        for smer in range(4):
            pattern = self.generate_path(smer)
            for i in pattern:
                print(*i)
            print()
            for r in range(8):
                for c in range(8):
                    if pattern[r][c] != -1:
                        if pattern[r][c] == Move.ATTACK:
                            self.sachovnica.itemconfig(self.parent.policka[r][c],fill=Color.ATTACK[(r+c)%2])
                        elif pattern[r][c] == Move.MOVE:
                            self.sachovnica.itemconfig(self.parent.policka[r][c],fill=Color.MOVE[(r+c)%2])
                        elif pattern[r][c] == Move.SHOOT:
                            self.sachovnica.itemconfig(self.parent.policka[r][c],fill=Color.SHOOT[(r+c)%2])

        self.sachovnica.itemconfig(self.parent.policka[self.y][self.x],fill=Color.SELECTED[(self.x + self.y)%2])


    # pohne figurku na x,y (ak sa da) a vrati ci sa da
    # TODO co ak mam viac moznosti? (shoot a move v inych smeroch vzdy)
    def move(self,x,y):
        print("MOVE TO",x,y)
        for smer in range(4):
            pattern = self.generate_path(smer)
            for i in pattern:
                print(*i)
            print()
            if self.parent.figurky[y][x] != None:
                # vyhodim figurku
                if pattern[y][x] in [Move.ATTACK, Move.ATTACK_AND_MOVE, Move.MOVE_AND_ATTACK]:
                    self.parent.figurky[y][x].delete()
                    self.parent.figurky[y][x], self.parent.figurky[self.y][self.x] = self.parent.figurky[self.y][self.x] ,self.parent.figurky[y][x]
                    self.sachovnica.move(self.id,(x - self.x)*SIZE,(y - self.y)*SIZE)
                    self.x, self.y = x,y
                    return 1
                # zastrelim figurku
                if pattern[y][x] == Move.SHOOT:
                    self.parent.figurky[y][x].delete()
                    return 1

            # viem sa tam pohnut
            elif pattern[y][x] == Move.MOVE:
                self.parent.figurky[y][x], self.parent.figurky[self.y][self.x] = self.parent.figurky[self.y][self.x] ,self.parent.figurky[y][x]
                self.sachovnica.move(self.id,(x - self.x)*SIZE,(y - self.y)*SIZE)
                self.x, self.y = x,y
                return 1
        print("neda sa zabit")
        return 0

    # reset vsetkych policok
    def deselect(self):
        for r in range(8):
            for c in range(8):
                self.sachovnica.itemconfig(self.parent.policka[r][c],fill=Color.DEFAULT[(r+c)%2])

    def delete(self):
        self.sachovnica.delete(self.id)
        self.parent.figurky[self.y][self.x] = None
        del(self)



root = tkinter.Tk()

sachovnica = Sachovnica(root)

sachovnica.test()

tkinter.mainloop()