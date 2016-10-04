# Random 4-way symmetrical logo generation a la GitHub
# Part of the New Scientist Live generator-generator
# Michael Cook (@mtrc) August 2016

import random
from PIL import Image, ImageDraw
import sys



# width = 300;
# height = 300;

# pixelswide = 10;
# pixelshigh = 10;

# pixelwidth = 30
# pixelheight = 30;

def generate_avatar(width, height, numpix, col=None):
    im = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    if col is None:
        col = (random.randrange(0, 255),random.randrange(0, 255),random.randrange(0, 255))

    for i in range(1,numpix):
        ox = random.randrange(0, width/2)
        oy = random.randrange(0, height/2)
        draw.rectangle([ox,oy, ox,oy], fill=col)
        #symmetric

        x = width - 1 - ox;
        y = oy

        draw.rectangle([x,y, x,y], fill=col)

        x = ox
        y = height - 1 - oy;

        draw.rectangle([x,y, x,y], fill=col)

        x = width  - ox - 1;
        y = height  - oy - 1;

        draw.rectangle([x,y, x,y], fill=col)
    return im

if __name__ == '__main__':

    im = generate_avatar(10,10,random.randrange(15, 20)).resize((300,300), Image.NEAREST)

    if len(sys.argv) > 1:
        filename = sys.argv[1]

    if len(sys.argv) == 1:
        im.show()
    else:
        im.save(filename)

