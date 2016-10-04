# Random crest generation
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

def load_palette():
    ps = open("palettes.txt", "r").readlines()
    p = random.choice(ps)
    cs = p.split("|")
    return cs

def randombut(fr, t, but):
    r = range(fr, but) + range(but+1, t)
    return random.choice(r)


def generate_quad(qn, h, cpal):
    quad = Image.new('RGBA', (300,h), literal_eval(cpal[qn]))
    if random.randrange(0, 2) == 0:
        # feat = Image.open("boys/animal"+str(random.randrange(1, 51))+".png")
        feat = animals.makeanimal().resize((300,300), Image.NEAREST)
    else:
        if random.randrange(0, 2) == 0:
            feat = symlogo.generate_avatar(10, 20, 40, literal_eval(cpal[randombut(0, 5, qn)]))#Image.open("avatars/avatar"+str(random.randrange(1, 101))+".png")
            feat = feat.resize((300,450), Image.NEAREST)
        else:
            feat = symlogo4.generate_avatar(10, 20, 30, literal_eval(cpal[randombut(0, 5, qn)]))#Image.open("avatars/avatar"+str(random.randrange(1, 101))+".png")
            feat = feat.resize((300,450), Image.NEAREST)
    quad.paste(feat, (0,0), feat)
    return quad

def gen_crest():

    cpal = load_palette()

    crest_base = Image.open("signs/crest_tall_full.png")
    crest_base = swap_color(crest_base, literal_eval(cpal[4]))

    # Crests have images in four quadrants, but we need a base to slap the crest on top of afterwards

    im = Image.new('RGBA', crest_base.size, (255, 255, 255, 0))

    quad = generate_quad(0, 300, cpal);
    im.paste(quad, (0,0), quad)

    quad = generate_quad(1, 300, cpal);
    im.paste(quad, (400,0), quad)

    quad = generate_quad(2, 500, cpal);
    im.paste(quad, (0,400), quad)

    quad = generate_quad(3, 500, cpal);
    im.paste(quad, (400,400), quad)

    # Finally, add on the crest on top
    im.paste(crest_base, (0,0), crest_base)

    return im

if __name__ == '__main__':
    im = gen_crest()

    if len(sys.argv) == 1:
        im.show()
    else:
        im.save(sys.argv[1])
