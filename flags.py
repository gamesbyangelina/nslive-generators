# Random flag generation
# Part of the New Scientist Live generator-generator
# Michael Cook (@mtrc) August 2016

import sys
import random
from PIL import Image, ImageDraw
import numpy as np
from ast import literal_eval
import symlogo, symlogo4, animals

def swap_color(img, toc):
    data = np.array(img)   # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    white_areas = (red == 255) & (blue == 255) & (green == 255)
    data[..., :-1][white_areas.T] = toc # Transpose back needed

    return Image.fromarray(data)

def h_stripes(im, ns, c):
    draw = ImageDraw.Draw(im)

    for i in range(0,ns):
        if i % 2 == 0:
            draw.rectangle([0,i*(im.size[1]/ns), im.size[0],(i+1)*(im.size[1]/ns)-1], fill=c)
    return im

def v_stripes(im, ns, c):
    draw = ImageDraw.Draw(im)

    for i in range(0,ns):
        if i % 2 == 0:
            draw.rectangle([i*(im.size[0]/ns),0, (i+1)*(im.size[0]/ns)-1, im.size[1]], fill=c)
    return im

def load_palette():
    ps = open("palettes.txt", "r").readlines()
    p = random.choice(ps)
    cs = p.split("|")
    return cs

def generate_layer(base, p):
    layer = Image.new('RGBA', (40,25), literal_eval(p[0]))

    key = random.randrange(0, 2)
    if key == 0:
        layer = v_stripes(layer, random.randrange(2, 8), literal_eval(p[1]))
    elif key == 1:
        layer = h_stripes(layer, random.randrange(2, 8), literal_eval(p[1]))

    key = random.randrange(0, 5)
    if key == 0:
        base.paste(layer, (0,0), layer)
    else:
        overlay = Image.open("flagparts/base"+str(random.randrange(2, 8))+".png")
        base.paste(layer, (0,0), overlay)
    return base

def generate_detail_layer(base, p):

    key = random.randrange(0, 2)
    if key == 0:
        #central
        layer = Image.open("flagparts/centre"+str(random.randrange(1, 3))+".png")
        layer = swap_color(layer, literal_eval(p))
        detail = animals.makeanimal()
        layer.paste(detail, (13, 5), detail)
    elif key == 1:
        #topleft
        layer = Image.open("flagparts/topleft"+str(random.randrange(1, 3))+".png")
        layer = swap_color(layer, literal_eval(p))
        detail = animals.makeanimal()
        layer.paste(detail, (0,0), detail)

    base.paste(layer, (0,0), layer)
    return base

def generate_flag():

    p = load_palette()

    base = Image.new('RGBA', (40,25), literal_eval(p[0]))

    base = generate_layer(base, p[1:3])

    if(random.randrange(0, 2)):
        base = generate_layer(base, p[3:5])
    else:
        base = generate_detail_layer(base, p[3])

    return base

if __name__ == '__main__':
    im = generate_flag().resize((600,375), Image.NEAREST)

    if len(sys.argv) == 1:
        im.show()
    else:
        im.save(sys.argv[1])
