# -*- coding: utf-8 -*-

import os
import sys
import pygame

from Game.settings import DISPLAY_MODE, START_TITLE_COLOR, START_TEXT_COLOR, BLACK, WHITE

#讓視窗居中
os.environ['SDL_VIDEO_WINDOW_POS'] = "center"

#MyGame默認值
GAME_NAME = "My Game"
SCREEN_SIZE = (640,480)
DISPLAY_MODE = pygame.HWSURFACE | pygame.DOUBLEBUF
LOOP_SPEED = 60
FONT_NAME = "Minecraft_font.ttf"
FONT_SIZE = 16
KEY_PAUSE = pygame.K_PAUSE

class MyGame(object):
    "pygame模板"
    def __init__(self,**kwargs):
        #初始化
        pygame.init()
        pygame.mixer.init() #初始化音效
        #遊戲標題與視窗設定
        self.game_name = kwargs.get("game_name") or GAME_NAME
        pygame.display.set_caption(self.game_name)
        self.screen_size = kwargs.get("screen_size") or SCREEN_SIZE
        self.screen_width, self.screen_height = self.screen_size
        self.display_mode = kwargs.get("display_mode") or DISPLAY_MODE
        self.icon = kwargs.get("icon") or None
        self.screen = pygame.display.set_mode(self.screen_size,self.display_mode)
        #遊戲速度與字體
        self.loop_speed = kwargs.get("loop_speed") or LOOP_SPEED
        self.font_name = kwargs.get("font_name") or FONT_NAME
        self.font_size = kwargs.get("font_size") or FONT_SIZE
        self.font = pygame.font.Font(self.font_name, self.font_size)
        self.clock = pygame.time.Clock()    #控制遊戲更新時間
        self.now = 0    #當前時間(毫秒)
        self.running = True #控制遊戲是否暫停
        #畫面更新
        self.background = pygame.Surface(self.screen_size)
        self.key_bindings = {}  #按鍵與函數綁定
        self.add_key_bind(KEY_PAUSE,self.pause)
        self.game_actions = {}  #遊戲數據更新動作
        self.draw_actions = [self._draw_background] #畫面更新動作列表
        self.draw = pygame.draw #快捷使用pygame.draw
        self.state = "start"    #封面畫面

    def run(self):
        """遊戲主循環"""
        while True:
            self.now = pygame.time.get_ticks()  #取得目前時間
            self._process_events()  #處理事件

            if self.state == "start":
                self._draw_background()    #畫背景
                self.draw_start_screen()   #畫封面
                pygame.display.flip()
                self.clock.tick(self.loop_speed)
                continue

            if self.running:
                self._update_gamedata()  #更新遊戲數據(例如蛇的移動)
            self._update_display()  #更新顯示
            self.clock.tick(self.loop_speed)

    def pause(self):
        """遊戲暫停"""
        self.running = not self.running
        if self.running:
            for action in self.game_actions.values():
                if action["next_time"]:
                    action["next_time"] = self.now + action["interval"]

    def switch_running(self):
        self.running = not self.running
        if self.running:
            for name, action in self.gamedata_update_actions.items():
                if action["next_time"]:
                    action["next_time"] = self.now + action["interval"]

    def _process_events(self):
        """處理使用者事件(案件,關閉視窗"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                #在封面狀態,按任何按鍵會進入遊戲
                if self.state == "start":
                    self.state = "running"  #從封面進入遊戲
                action,kwargs = self.key_bindings.get(event.key,(None,None))
                action(**kwargs) if kwargs else action() if action else None

    def _update_gamedata(self):
        """處理需要定時更新的動作(像是蛇移動)"""
        for action in self.game_actions.values():
            if not action["next_time"]:
                action["run"]()
            elif self.now >= action["next_time"]:
                action["next_time"] += action["interval"]
                action["run"]()

    def _update_display(self):
        """更新畫面"""
        for action in self.draw_actions:
            action()
        pygame.display.flip()

    def _draw_background(self):
        """將背景畫到螢幕上"""
        self.screen.blit(self.background,(0,0))

    def add_key_bind(self,key,action,**kwargs):
        """設定按鍵對應動作"""
        self.key_bindings[key] = action,kwargs

    def add_game_action(self,name,action,interval=0):
        """加入遊戲動作"""
        next_time = self.now + interval if interval else None
        self.game_actions[name] = dict(run=action,interval=interval,next_time=next_time)

    def add_draw_action(self,action):
        """加入繪圖動作(每幀執行)"""
        self.draw_actions.append(action)

    def draw_text(self,text,loc,color,bgcolor=None,center=False):
        """畫出文字"""
        if bgcolor:
            surface = self.font.render(text,True,color,bgcolor)
        else:
            surface = self.font.render(text,True,color)
        if center:
            rect = surface.get_rect(center=loc)
        else:
            rect = surface.get_rect(topleft=loc)

        self.screen.blit(surface,rect)

    def draw_cell(self,xy,size,color1,color2=None):
        """畫出格子"""
        x,y = xy
        rect = pygame.Rect(x*size,y*size,size,size)
        self.screen.fill(color1,rect)
        if color2:
            inner_rect = rect.inflate(-4, -4)   #內部小一點
            self.screen.fill(color2, inner_rect)


    def quit(self):
        """關閉遊戲"""
        pygame.quit()
        sys.exit(0)

    def draw_start_screen(self):
        title = "Snake Game"
        start_msg = "Press any key to start"

        # 建立文字表面
        title_surface = self.font.render(title, True, START_TITLE_COLOR)
        msg_surface = self.font.render(start_msg, True,WHITE,BLACK)

        # 置中位置
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 60))
        msg_rect = msg_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 30))

        # 畫到畫面
        self.screen.blit(title_surface, title_rect)
        self.screen.blit(msg_surface, msg_rect)

#測試用
if __name__ == "__main__":
    MyGame().run()