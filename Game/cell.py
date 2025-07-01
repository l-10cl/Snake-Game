# -*- coding: utf-8 -*-

class Cell(object):
    "方塊"
    def __init__(self, x, y,color1,color2):
        self.x = x
        self.y = y
        self.color1 = color1
        self.color2 = color2

    def move(self,dx,dy):
        self.x += dx
        self.y += dy