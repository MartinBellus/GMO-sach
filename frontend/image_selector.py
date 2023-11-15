import os
from PIL import Image,ImageTk
from utility.enums import colors
from utility.constants import *

def adjust(px : tuple,color : colors):
    if color == colors.WHITE:
        const = 0.5
    else:
        const = 1.5
    return (int(px[0]*const),int(px[1]*const),int(px[2]*const),px[3])

class ImageSelector:
    images : list[Image.Image] = []
    def __init__(self,width : int = 50,height : int = 50):
        # load all images
        for file in os.listdir(IMAGE_DIR):
            try:
                self.images.append(Image.open(IMAGE_DIR + file).resize((width,height)))
            except Exception as ex:
                print(ex)

    def get_image(self,hash : str,color : colors) -> ImageTk.PhotoImage:
        int_hash = int(hash,36)
        img = self.images[int_hash%len(self.images)]
        new_image_raw : list[tuple]= []
        for px in img.getdata():
            new_image_raw.append(adjust(px,color))
        ret_img = Image.new(img.mode,img.size)
        ret_img.putdata(new_image_raw)
        return ImageTk.PhotoImage(ret_img)