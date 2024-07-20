import os
from PIL import Image,ImageTk
from backend.chessboard import PieceInfo
from utility.enums import colors
from utility.constants import *

def adjust(px : tuple[int,int,int,int],color : colors):
    """
    Adjust colors of image pixel based on piece color

    Args:
        px : pixel
        color : color of piece
    """
    if color == colors.WHITE:
        const = 1.5
    else:
        const = 0.5
    return (int(px[0]*const),int(px[1]*const),int(px[2]*const),px[3])

class ImageSelector:
    """
    Class that selects images for pieces
    """
    images : list[Image.Image] = []
    special : dict[str, Image.Image] = {}
    def __init__(self,width : int = 50,height : int = 50):
        # load all images
        for file in os.listdir(IMAGE_DIR):
            try:
                image = Image.open(IMAGE_DIR + file)
                image.getdata()[0][3]
                self.images.append(Image.open(IMAGE_DIR + file).resize((width,height)))
            except Exception as ex:
                print(f"Can not open {file}: {ex}")

        # load all special images
        for file in os.listdir(IMAGE_DIR + "special/"):
            try:
                self.special[file[:-4]] = Image.open(IMAGE_DIR + "special/" + file).resize((width,height))
                print(file[:-4])
            except Exception as ex:
                print(f"Can not open {file}: {ex}")

    def get_image(self,piece : PieceInfo) -> ImageTk.PhotoImage:
        """
        Get image for piece based on piece color and genome hash

        Params:
            piece
        """
        int_hash = int(piece.genome_hash,36)
        img = self.images[int_hash%len(self.images)]
        new_image_raw : list[tuple]= []
        for px in img.getdata():
            new_image_raw.append(adjust(px,piece.color))
        ret_img = Image.new(img.mode,img.size)
        ret_img.putdata(new_image_raw)
        if piece.is_king:
            ret_img.paste(self.special["king"],(0,0),self.special["king"])
        return ImageTk.PhotoImage(ret_img)
