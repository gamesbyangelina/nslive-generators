# An outfit generator (possibly expanded to cover dolls?)
# Part of the New Scientist Live generator-generator
# Michael Cook (@mtrc) August 2016

import sys, re
import random
from PIL import Image, ImageDraw
import numpy as np
from ast import literal_eval
import patterns

def swap_color(img, toc):
    data = np.array(img)   # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    white_areas = (red == 255) & (blue == 255) & (green == 255)
    data[..., :-1][white_areas.T] = toc # Transpose back needed

    return Image.fromarray(data)

def load_palette():
    ps = open("palettes.txt", "r").readlines()
    p = random.choice(ps)
    cs = [ literal_eval(x) for x in p.split("|")[:-1] ]
    return cs

def make_clothes():
    pal = load_palette()
    im = Image.new('RGBA', (160, 320), (0,0,0,0))

    body = Image.open("clothes/body.png")
    body = body.resize((160,320), Image.NEAREST)
    im.paste(body, (0,0), body)

    #pick shoes
    shoes = Image.open("clothes/shoes"+str(random.randrange(1, 6))+".png")
    shoes = swap_color(shoes, pal[1])
    shoes = shoes.resize((160,320), Image.NEAREST)
    im.paste(shoes, (0,0), shoes)

    #pick bottoms
    bottom = Image.open("clothes/bottom"+str(random.randrange(1, 7))+".png")
    bottom = swap_color(bottom, pal[2])
    bottom = bottom.resize((160,320), Image.NEAREST)

    pattern = patterns.generate_pattern(135,135,7,load_palette()).resize((540,540),Image.NEAREST).crop((0,0,160,320))
    im.paste(pattern, (0,0), bottom)

    #pick tops
    top = Image.open("clothes/top"+str(random.randrange(1, 5))+".png")
    top = swap_color(top, pal[3])
    top = top.resize((160,320), Image.NEAREST)

    pattern = patterns.generate_pattern(135,135,7,load_palette()).resize((540,540),Image.NEAREST).crop((0,0,160,320))
    im.paste(pattern, (0,0), top)

    #pick hats
    hat = Image.open("clothes/hat"+str(random.randrange(1, 6))+".png")
    hat = swap_color(hat, pal[4])
    hat = hat.resize((160,320), Image.NEAREST)
    im.paste(hat, (0,0), hat)

    return im

if __name__ == '__main__':
    im = make_clothes()

    if len(sys.argv) == 1:
        im.show()
    else:
        im.save(sys.argv[1])
