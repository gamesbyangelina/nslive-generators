# Random symmetrical logo generation a la GitHub
# Part of the New Scientist Live generator-generator
# Michael Cook (@mtrc) August 2016

import random
from PIL import Image, ImageDraw
import sys

from StringIO import StringIO

if len(sys.argv) > 1:
    filename = sys.argv[1]

# width = 300;
# height = 300;

# pixelswide = 10;
# pixelshigh = 10;

# pixelwidth = 30
# pixelheight = 30;

def saveToTemp(im):
    # tempFileObj = NamedTemporaryFile(mode='w+b',suffix='jpg')
    # pilImage = open('outfile.jpg','rb')
    # copyfileobj(im,tempFileObj)
    # pilImage.close()
    # remove('outfile.jpg')
    # tempFileObj.seek(0,0)
    img_io = StringIO()
    im.save(img_io, 'png')
    img_io.seek(0)
    return img_io

def generate_avatar(width, height, numpix, col=None):
    im = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    if col is None:
        col = (random.randrange(0, 255),random.randrange(0, 255),random.randrange(0, 255))

    for i in range(1, numpix):
        x = random.randrange(0, width/2)
        y = random.randrange(0, height)
        draw.rectangle([x,y, x,y], fill=col)
        #symmetric

        x = width - x - 1;

        draw.rectangle([x,y, x,y], fill=col)

    return im

if __name__ == '__main__':
    im = generate_avatar(10,10,random.randrange(15, 20)).resize((300,300), Image.NEAREST)

    if len(sys.argv) == 1:
        im.show()
    else:
        im.save(filename)

