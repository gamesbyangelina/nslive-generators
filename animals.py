# Random animal generation using body part snapping
# Part of the New Scientist Live generator-generator
# Michael Cook (@mtrc) August 2016

import sys
import random
from PIL import Image, ImageDraw
import numpy as np
from ast import literal_eval

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

def makeanimalfamily():
    im = Image.new('RGBA', (50, 30), (255, 255, 255, 0))
    animal = makeanimal()
    im.paste(animal, (2, 15), animal)
    animal = animal.transpose(Image.FLIP_LEFT_RIGHT)
    im.paste(animal, (38, 15), animal)
    animal = animal.resize((24,24), Image.NEAREST)
    im.paste(animal, (14, 3), animal)
    return im

def makeanimal():
    cs = load_palette()
    legcolor = literal_eval(cs[0])
    bodycolor = literal_eval(cs[1])
    headcolor = literal_eval(cs[2])
    earcolor = literal_eval(cs[3])
    facecolor = literal_eval(cs[4])

    numfaces = 6
    numbodies = 6
    numlegs = 5
    numears = 5
    numheads = 5

    width = 300;
    height = 300;

    pixelswide = 12;
    pixelshigh = 12;

    pixelwidth = 25;
    pixelheight = 25;

    im = Image.new('RGBA', (pixelswide, pixelshigh), (255, 255, 255, 0))

    legs = Image.open("bodyparts/legs"+str(random.randrange(1, numlegs+1))+".png")
    legs = swap_color(legs, legcolor)
    lwidth, lheight = legs.size

    legsy = pixelshigh - lheight;
    legsx = pixelswide/2 - lwidth/2;

    im.paste(legs, (legsx, legsy), legs)

    body = Image.open("bodyparts/body"+str(random.randrange(1, numbodies+1))+".png")
    body = swap_color(body, bodycolor)
    #dimensions
    bwidth, bheight = body.size

    body_connections_below = []
    for i in range(0, bwidth):
        r, g, b, a = body.getpixel((i, bheight-1))
        body_connections_below.append(a > 0)

    bodyx = pixelswide/2 - bwidth/2
    bodyy = legsy-bheight + random.randrange(0, 2)

    # print lheight
    # print legsy
    # print bheight

    # check the legs match up
    for i in range(0, lwidth):
        r, g, b, a = legs.getpixel((i, 0))
        if a > 0:
            if (i + legsx - bodyx < 0) or (i + legsx - bodyx) > bwidth-1:
                return makeanimal()
            r,g,b,a = body.getpixel((i + legsx - bodyx, bheight-1))
            if a == 0:
                return makeanimal()

    im.paste(body, (bodyx, bodyy), body)

    #list places body connects above
    body_connections_top = []
    for i in range(0, bwidth):
        r, g, b, a = body.getpixel((i, 0))
        body_connections_top.append(a > 0)

    head = Image.open("bodyparts/head"+str(random.randrange(1, numheads+1))+".png")
    head = swap_color(head, headcolor)
    #dimensions
    hwidth, hheight = head.size

    #list places head connects below
    head_connections_below = []
    for i in range(0, hwidth):
        r, g, b, a = head.getpixel((i, 0))
        head_connections_below.append(a > 0)

    #keep looking for spots until we find a good place
    good = False
    heady = bodyy-hheight+1
    tries = 0
    while(not good and tries < 100):
        good = True
        headx = random.randrange(0, pixelswide)
        has_connection_point = False;
        for i in range(0, hwidth):
            cpoint = headx + i - bodyx
            if cpoint >= 0 and cpoint+hwidth < pixelswide-1 and cpoint < bwidth and body_connections_top[cpoint] and head_connections_below[i]:
                has_connection_point = True;
        good = has_connection_point
        tries = tries + 1

    im.paste(head, (headx, heady), head)



    face = Image.open("bodyparts/face"+str(random.randrange(1, numfaces+1))+".png")
    face = swap_color(face, facecolor)
    #dimensions
    fwidth, fheight = face.size

    facex = headx + (hwidth/2 - fwidth/2)
    facey = heady + hheight - fheight

    for i in range(0, fwidth):
        for j in range(0, fheight):
            if i-facex+headx >= 0 and i-facex+headx < fwidth-1 and j-facey+heady >= 0 and j-facey+heady < fheight-1:
                # print i-facex+headx
                # print j-facey+heady
                r, g, b, a = head.getpixel((i-facex+headx, j-facey+heady))
                if a == 0:
                    return makeanimal()

    im.paste(face, (facex, facey), face)

    ears = Image.open("bodyparts/ears"+str(random.randrange(1, numears+1))+".png")
    ears = swap_color(ears, earcolor)
    ewidth, eheight = ears.size
    if(ewidth > hwidth):
        return makeanimal()

    earsx = headx
    if ewidth < hwidth:
        earsx + random.randrange(0, hwidth-ewidth)
    earsy = heady-eheight

    im.paste(ears, (earsx, earsy), ears)

    return im


if __name__ == '__main__':
    im = makeanimal().resize((300,300), Image.NEAREST)

    if len(sys.argv) == 1:
        im.show()
    else:
        im.save(sys.argv[1])
