# -*- coding: utf-8 -*-

import pygame
from settings import *

class Field(object):
    "場地"

    def __init__(self,game,columns,rows):
        self.game = game    #取得主遊戲物件
        self.screen = self.game.screen  #畫面物件
        self.columns = columns  #欄數(橫向)
        self.rows = rows    #列數(縱向)
        #建立一個二微陣列來記錄每個格子上的cell(蛇和食物)
        self.cell_array = [[None] * self.columns for i in range(self.rows)]
        #加入繪圖動作
        self.game.add_draw_action(self.draw)

    def put_cell(self,cell):
        """放置方塊"""
        if 0 <= cell.x < self.columns and 0 <= cell.y < self.rows:
            self.cell_array[cell.y][cell.x] = cell

    def get_cell(self,x,y):
        """取得方塊"""
        if 0 <= x < self.columns and 0 <= y < self.rows:
            return self.cell_array[y][x]
        else:
            return OUT

    def del_cell(self,x,y):
        """刪除方塊"""
        if 0 <= x < self.columns and 0 <=y < self.rows:
            self.cell_array[y][x] = None

    def draw_cell(self):
        """繪製場地"""
        for row in self.cell_array:
            for cell in row:
                if cell:
                    rect = pygame.Rect(cell.x*CELL_SIZE,cell.y*CELL_SIZE,CELL_SIZE,CELL_SIZE)
                    self.screen.fill(cell.color1,rect)
                    self.screen.fill(cell.color2,rect.inflate(-4,-4))

    def clear(self):
        """清空場地"""
        self.cell_array = [[None] * self.columns for i in range(self.rows)]