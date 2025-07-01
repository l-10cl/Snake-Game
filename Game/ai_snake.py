# -*- coding: utf-8 -*-

import pygame
from settings import *
from random import choice

class AISnake:
    """AI 貪吃蛇"""

    def __init__(self, game):
        self.game = game                    # 取得遊戲主程式的參考
        self.alive = True                   # AI 蛇是否存活
        self.head = (COLUMNS - 5, ROWS - 5) # 初始蛇頭位置（右下角附近）
        self.body = [(-1, -1)] * SNAKE_BODY_LENGTH  # 初始蛇身
        self.direction = LEFT               # 初始方向
        self.new_direction = self.direction # 準備變更的方向
        self.speed = SNAKE_SPEED            # 初始速度
        self.move_interval = 1000 // self.speed  # 每幾毫秒移動一次
        self.last_move_time = pygame.time.get_ticks()  # 上次移動時間
        self.game.add_draw_action(self.draw)          # 加入繪圖動作

    def draw(self):
        """畫出 AI 蛇"""
        skin_color = AI_SNAKE_COLOR_SKIN if self.alive else SNAKE_COLOR_SKIN_DEAD
        body_color = AI_SNAKE_COLOR_BODY if self.alive else SNAKE_COLOR_BODY_DEAD
        head_color = AI_SNAKE_COLOR_HEAD if self.alive else SNAKE_COLOR_HEAD_DEAD
        for cell in self.body:
            self.game.draw_cell(cell, CELL_SIZE, skin_color, body_color)
        self.game.draw_cell(self.head, CELL_SIZE, skin_color, head_color)

    def move(self):
        """AI 蛇的移動邏輯"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < self.move_interval:
            return  # 尚未到移動時間

        self.last_move_time = current_time

        if not self.alive:
            return  # 死掉不移動

        self.choose_direction()  # AI 自動選擇方向
        self.direction = self.new_direction

        # 計算新頭的位置
        next_head = (self.head[0] + self.direction[0], self.head[1] + self.direction[1])
        x, y = next_head

        # 判斷是否死亡（撞牆、撞自己、撞玩家）
        if next_head in self.body or \
           next_head == self.game.snake.head or \
           next_head in self.game.snake.body or \
           x not in range(COLUMNS) or y not in range(ROWS):
            self.die()
            return

        # 吃到食物
        if next_head == (self.game.food.x, self.game.food.y):
            self.game.food.drop()   # 重生食物
            self.game.ai_score += 1  # AI 記錄吃到的數量

            # 每吃5個就加速
            if self.game.ai_score % 5 == 0:
                self.speed_up()
                self.move_interval = max(100, self.move_interval - 50)
        else:
            self.body.pop()  # 沒吃到就移動：尾巴減一格

        self.body = [self.head] + self.body  # 將原來的頭加入身體
        self.head = next_head                # 移動頭部

    def choose_direction(self):
        """AI 簡單邏輯：朝食物方向移動"""
        food_x, food_y = self.game.food.x, self.game.food.y
        head_x, head_y = self.head

        # 建立可選方向
        directions = []

        if food_x < head_x:
            directions.append(LEFT)
        elif food_x > head_x:
            directions.append(RIGHT)
        if food_y < head_y:
            directions.append(UP)
        elif food_y > head_y:
            directions.append(DOWN)

        # 確保選項有備用方向
        all_dirs = [UP, DOWN, LEFT, RIGHT]
        for d in all_dirs:
            if d not in directions:
                directions.append(d)

        # 嘗試每個方向，找到沒撞牆或撞蛇的合法方向
        for d in directions:
            nx = head_x + d[0]
            ny = head_y + d[1]
            if 0 <= nx < COLUMNS and 0 <= ny < ROWS:
                next_pos = (nx, ny)
                if next_pos not in self.body and next_pos not in self.game.snake.body:
                    self.new_direction = d
                    return

        # 如果都不行就維持原方向（可能會撞）
        self.new_direction = self.direction

    def die(self):
        """AI 蛇死亡"""
        self.alive = False

    def respawn(self):
        """AI 蛇重生"""
        self.head = (COLUMNS - 5, ROWS - 5) #預設從右下角開始
        self.body = [(-1, -1)] * SNAKE_BODY_LENGTH  #初始蛇身
        self.direction = LEFT
        self.new_direction = LEFT
        self.speed = SNAKE_SPEED
        self.move_interval = 1000 // self.speed #移動間隔
        self.last_move_time = pygame.time.get_ticks()
        self.alive = True

    def speed_up(self):
        """AI 蛇加速"""
        if self.speed < 20:
            self.speed += 1
            self.move_interval = max(100, 1000 // self.speed)