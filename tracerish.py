# A knockoff tracery reimplementation in python
# Part of the New Scientist Live generator-generator
# Michael Cook (@mtrc) August 2016

import sys, re
import random
from PIL import Image, ImageDraw
import numpy as np
from ast import literal_eval

tracery_object = {
    "start" : ["The #animal# And #animal#", "The #adjective# #animal#"],
    "animal" : ["Owl", "Pussycat", "Labradoodle", "Lion", "Llama", "Donkey"],
    "adjective" : ["Laughing", "Dancing", "Winking", "Hopping", "Sleeping"]
}

file_names = {
    "filename" : ["#adjective#-#animal#"],
    "adjective" : ["Brutal", "Exuberant", "Awesome", "Fantastic", "Dour", "Frantic", "Jocular", "Prim", "Teetotal", "Worried", "Jumping", "Dancing", "Laughing", "Smiling", "Guffawing"],
    "animal" : ["Rhino", "Flamingo", "Albatross", "Bugbear", "Hare", "Lion", "Gorilla", "Lynx", "Zebra"]
}

def process_raw(obj):
    nd = {}
    for key, value in obj.items():
        nd[key] = value[0].split(",")
    return nd

def execute_rule(obj, tgt):
    # print obj[tgt]
    pick = random.choice(obj[tgt])
    #does pick contain any words that need to be expanded?
    expansions = re.findall(r'\#([^\#]*)\#', pick)
    for expansion in expansions:
        pick = pick.replace("#"+expansion+"#", execute_rule(obj, expansion), 1)
    return pick

# print execute_rule(file_names, "filename")
