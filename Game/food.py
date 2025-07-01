# -*- coding: utf-8 -*-

from settings import *
from random import randint


class Food(object):
    """食物"""

    def __init__(self,game):
        self.game = game    #取得主遊戲物件
        self.x = self.y = 0 #食物初始位置
        self.game.add_draw_action(self.draw)    #畫圖動作
        self.drop()     #隨機放食物

    def drop(self):
        """生成新的食物"""
        if not hasattr(self.game, "snake") or not hasattr(self.game.snake, "body"):
            return  #如果蛇還沒建立好就跳過
        snake = self.game.snake.body + [self.game.snake.head]
        while True:
            (x,y) = randint(0,COLUMNS-1),randint(0,ROWS-1)
            if (x,y) not in snake:
                self.x,self.y = x,y
                break

    def draw(self):
        """繪製食物"""
        self.game.draw_cell((self.x,self.y),CELL_SIZE,FOOD_COLOR_SKIN,FOOD_COLOR_BODY)