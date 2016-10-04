# Tiled pattern generator
# Part of the New Scientist Live generator-generator
# Michael Cook (@mtrc) August 2016

import sys
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap
import numpy as np
from ast import literal_eval

def swap_color(img, toc):
    data = np.array(img)   # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    white_areas = (red == 255) & (blue == 255) & (green == 255)
    data[..., :-1][white_areas.T] = toc # Transpose back needed

    return Image.fromarray(data)

def generate_tile(type, size, palette, chance):
    im = Image.new('RGBA', (size,size), (0,0,0,0))
    draw = ImageDraw.Draw(im)

    if type == 0:
        if random.uniform(0, 1) < chance[0]:
            for i in range(0, size):
                draw.rectangle([i,i,i,i], fill=palette[0])
        elif random.uniform(0, 1) < chance[1]:
            for i in range(0, size):
                draw.rectangle([size-i-1,i,size-i-1,i], fill=palette[1])

    # works best with odd-sized tiles
    if type == 1:
        size = size + 2
        im = Image.new('RGBA', (size,size), (0,0,0,0))
        draw = ImageDraw.Draw(im)
        if random.uniform(0, 1) < chance[0]:
            for i in range(0, size/2+1):
                draw.rectangle([i,i,i,i], fill=palette[0])
        if random.uniform(0, 1) < chance[1]:
            for i in range(0, size/2+1):
                draw.rectangle([size-1-i,i,size-1-i,i], fill=palette[1])
        if random.uniform(0, 1) < chance[2]:
            for i in range(size/2, size):
                draw.rectangle([i,i,i,i], fill=palette[2])
        if random.uniform(0, 1) < chance[3]:
            for i in range(size/2, size):
                draw.rectangle([size-1-i,i,size-1-i,i], fill=palette[3])

    if type == 2:
        if random.uniform(0, 1) < chance[0]:
            draw.rectangle([size/2,0,size/2,size], fill=palette[0])
        if random.uniform(0, 1) < chance[1]:
            draw.rectangle([0,size/2,size,size/2], fill=palette[1])


    return im

def generate_tileable_shape(size, p):
    im = Image.new('RGBA', (size*3,size*3), (0,0,0,0))

    for i in range(1, random.randrange(8, 20)):
        #load shape
        shape = Image.open("symbols/shape"+str(random.randrange(1, 8))+".png")
        shape = swap_color(shape, p[random.randrange(len(p)-1)])
        #draw the shape nine times somewhere
        x = random.randrange(-shape.size[0], size)
        y = random.randrange(-shape.size[1], size)# + shape.size[1])

        im.paste(shape, (x-size,y-size), shape)
        im.paste(shape, (x-size,y), shape)
        im.paste(shape, (x-size,y+size), shape)
        im.paste(shape, (x,y-size), shape)
        im.paste(shape, (x,y), shape)
        im.paste(shape, (x,y+size), shape)
        im.paste(shape, (x+size,y-size), shape)
        im.paste(shape, (x+size,y), shape)
        im.paste(shape, (x+size,y+size), shape)

    x = random.randrange(0, size)
    y = random.randrange(0, size)
    #get a random offset and crop
    im = im.crop((x,y,x+size,y+size))

    return im

def generate_pattern(width, height, tilesize, p):
    im = Image.new('RGBA', (width,height), p[0])

    tilepal = [p[random.randrange(1,5)],p[random.randrange(1,5)],p[random.randrange(1,5)],p[random.randrange(1,5)]];
    chances = [random.uniform(0.2, 0.8),random.uniform(0.2, 0.8),random.uniform(0.2, 0.8),random.uniform(0.2, 0.8)]
    type = random.randrange(0,4)

    if type == 3:
        tilesize = tilesize * 4
        tile = generate_tileable_shape(tilesize, p)

    for i in range(-1,width/tilesize+1):
        for j in range(-1, height/tilesize+1):
            if type == 3:
                x = 10
            else:
                tile = generate_tile(type, tilesize, tilepal, chances)

            if type == 1:
                im.paste(tile, (i*(tilesize+2)-i, j*(tilesize+2)-j), tile)
            else:
                im.paste(tile, (i*tilesize, j*tilesize), tile)

    return im

def load_palette():
    ps = open("palettes.txt", "r").readlines()
    p = random.choice(ps)
    cs = map(literal_eval, p[:-2].split("|"))
    return cs

if __name__ == '__main__':
    im = generate_pattern(135,135,7,load_palette()).resize((540,540), Image.NEAREST)

    if len(sys.argv) == 1:
        im.show()
    else:
        im.save(sys.argv[1])
