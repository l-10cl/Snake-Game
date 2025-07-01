# -*- coding: utf-8 -*-

from settings import *
import pygame
from random import randint
from game import MyGame

class Snake(object):
    """貪吃蛇"""

    def __init__(self,game):
        self.game = game
        self.alive = True
        self.head = (SNAKE_X, SNAKE_Y)
        self.body = [(-1,-1)]*SNAKE_BODY_LENGTH
        self.move_interval = 500
        self.last_move_time = pygame.time.get_ticks()   #紀錄上次移動時間
        self.direction = RIGHT
        self.new_direction = SNAKE_DIRECTION
        self.speed = SNAKE_SPEED
        self.sound_hit = pygame.mixer.Sound('hit.wav')
        self.sound_eat = pygame.mixer.Sound('eat.wav')
        self.game.add_draw_action(self.draw)
        self.respawn()


    def set_speed(self,speed):
        """設定蛇的速度和控制移動頻率"""
        self._speed = speed
        interval = 1000 / self._speed   #計算移動間隔
        self.game.add_game_action("snake.move",self.move,interval)

    def get_speed(self):
        """取得蛇的速度"""
        return self._speed

    def draw(self):
        """畫出蛇"""
        skin_color = SNAKE_COLOR_SKIN if self.alive else SNAKE_COLOR_SKIN_DEAD
        body_color = SNAKE_COLOR_BODY if self.alive else SNAKE_COLOR_BODY_DEAD
        head_color = SNAKE_COLOR_HEAD if self.alive else SNAKE_COLOR_HEAD
        for cell in self.body:
            self.game.draw_cell(cell,CELL_SIZE,skin_color,body_color)
        self.game.draw_cell(self.head,CELL_SIZE,skin_color,head_color)

    def turn(self,**kwargs):
        """控制蛇轉向"""
        if (self.direction in [LEFT,RIGHT] and kwargs["direction"] in [UP,DOWN] or self.direction in[UP,DOWN]
        and kwargs["direction"] in [LEFT,RIGHT]):
            self.new_direction = kwargs["direction"]

    def move(self):
        """蛇的移動"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time>=self.move_interval:
            self.last_moe_time = current_time


        if self.alive:
            #改變方向
            self.direction = self.new_direction

            #探測下一個位置的物體
            x,y = meeting = (self.head[0] + self.direction[0], self.head[1] + self.direction[1])

            #死亡
            if meeting in self.body or \
                    meeting in self.game.snake.body or \
                    meeting == self.game.snake.head or \
                    meeting in self.game.ai_snake.body or \
                    meeting == self.game.ai_snake.head or \
                    x not in range(COLUMNS) or y not in range(ROWS):
                self.die()
                return



            #判斷是否吃了食物
            if meeting == (self.game.food.x, self.game.food.y):
                self.sound_eat.play()
                self.game.food.drop()
                self.game.food_counter += 1
                #每吃5個加速
                if self.game.food_counter % 5 == 0:
                    self.speed_up()
                    self.move_interval = max(100,self.move_interval-50)

            else:
                self.body.pop()

            #增加一節身體
            self.body = [self.head] + self.body

            #移動蛇頭
            self.head = meeting


    speed = property(get_speed,set_speed)

    def speed_up(self):
        if self.speed < 20:
            self.speed += 1
            self.set_speed(self.speed)

    def speed_down(self):
        if self.speed > 1:
            self.speed -= 1

    def die(self):
        """蛇的死亡"""
        self.sound_hit.play()
        self.alive = False

    def respawn(self):
        #重生
        if not self.alive:
            self.head = (SNAKE_X,SNAKE_Y)
            self.body = [(-1,-1)] * SNAKE_BODY_LENGTH
            self.direction = SNAKE_DIRECTION
            self.new_direction = SNAKE_DIRECTION
            self.speed = SNAKE_SPEED
            self.alive = True


