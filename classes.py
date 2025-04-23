'''
classes.py - multiple classes for cano.py simulations

Student Name - Miguel Pereira
Student ID   - 22646169

Version History:
    - 6/10/24 - original version created
    - 6/10/24 - final version finished

'''
import numpy as np

class Block():

    def __init__(self, size, topleft):
        self.size = size        # size of Block square
        self.topleft = topleft  # (x,y) coord of topleft of Block
        self.items = []         # empty list to hold items

    def add_item(self, item):
        self.items.append(item)

    def __str__(self):
        return f"Block: {self.topleft}, #items = {len(self.items)}"

class Tree():

    def __init__(self, pos, colourtemp, size):
        self.pos = pos
        self.colourtemp = colourtemp
        self.size = size

class House():

    def __init__(self, pos, colourtemp, orientation):
        self.pos = pos
        self.colourtemp = colourtemp
        self.orientation = orientation