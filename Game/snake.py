# -*- coding: utf-8 -*-

from settings import *
from game import MyGame
from pysnake import Snake
from food import Food
from ai_snake import AISnake


class snake(MyGame):
    """貪吃蛇遊戲"""

    def __init__(self):
        """初始化"""
        super(snake,self).__init__(game_name=GAME_NAME,icon=ICON,screen_size=SCREEN_SIZE,display_mode=DISPLAY_MODE,
                                   loop_speed=LOOP_SPEED,font_name=FONT_NAME,font_size=FONT_SIZE,)
        #繪製背景
        self.prepare_background()
        #初始化遊戲物件
        self.food_counter = 0
        self.snake = Snake(self)
        self.food = Food(self)
        self.high_score = self.load_high_score()

        #控制按鍵設定
        self.add_key_bind(KEY_UP,self.snake.turn,direction=UP)
        self.add_key_bind(KEY_DOWN, self.snake.turn,direction=DOWN)
        self.add_key_bind(KEY_LEFT, self.snake.turn,direction=LEFT)
        self.add_key_bind(KEY_RIGHT, self.snake.turn,direction=RIGHT)
        self.add_key_bind(KEY_RESTART, self.restart)
        self.add_key_bind(KEY_EXIT, self.quit)

        #顯示分數
        self.add_draw_action(self.show_score)

        #讀取歷史最高分
        self.high_score = self.load_high_score()

        #AI蛇
        self.ai_snake = AISnake(self)
        self.ai_score = 0

    def prepare_background(self):
        """設定背景畫面"""
        self.background.fill(BACKGROUND_COLOR)
        for _ in range(CELL_SIZE,SCREEN_WIDTH,CELL_SIZE):
            self.draw.line(self.background,GIRD_COLOR,(_,0),(_,SCREEN_HEIGHT))
        for _ in range(CELL_SIZE,SCREEN_HEIGHT,CELL_SIZE):
            self.draw.line(self.background,GIRD_COLOR,(0,_),(SCREEN_WIDTH,_))

    def restart(self):
        """重新開始遊戲"""
        if not self.snake.alive:
            self.food_counter = 0
            self.food.drop()
            self.snake.respawn()
            self.running = True
            self.ai_snake.respawn()
            self.ai_score = 0

    def show_score(self):
        """顯示分數"""
        text = "Score %d" % self.food_counter
        self.draw_text(text,(0,0),(255,255,33))

        if not self.snake.alive:
            self.draw_text(" Game Over ", (SCREEN_WIDTH / 2 - 60, SCREEN_HEIGHT / 2 - 30), (255, 33, 33), WHITE)
            self.draw_text(" press R to restart ", (SCREEN_WIDTH / 2 - 90, SCREEN_HEIGHT / 2 + 10),
                           (33, 33, 33), GREY)

        if not self.running and self.snake.alive:
            self.draw_text(" GAME PAUSED ",SCREEN_WIDTH//2,SCREEN_HEIGHT/2-10,
                           (255,33,33),LIGHT_GREY,DARK_GREY)
        text_high = "High Score %d" % self.high_score
        self.draw_text(text_high,(0,20),HIGH_SCORE_COLOR)

    def _update_gamedata(self):
        super()._update_gamedata()  #保證玩家蛇正常移動
        if self.snake.alive:
            self.ai_snake.move()    #更新AI蛇的位置

        if not self.snake.alive and self.food_counter > self.high_score:
            self.high_score = self.food_counter
            self.save_high_score()

    def load_high_score(self):
        """讀取歷史最高分"""
        try:
            with open(HISCORE_FILE,"r") as file:
                return int(file.read())
        except:
            return 0    #讀取不到就回傳0

    def save_high_score(self):
        """儲存新的歷史最高分"""
        with open(HISCORE_FILE,"w") as file:
            file.write(str(self.high_score))

if __name__ == "__main__":
    snake().run()

