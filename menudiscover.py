import pygame
from ButtonDiscover import ButtonDiscover
from menu import Menu
from SimpleButtons import ButtonShowMap
from ButtonCancel import ButtonCancel
from Color import *
from ButtonSkip import ButtonSkip

class MenuDiscover(Menu):
  def __init__(self, bot, maze, screen, speed, list_menu):
    super().__init__(list_menu)
    self.state = True
    self.bot = bot
    self.maze = maze
    self.screen = screen
    self.btn_dfs = ButtonDiscover(alg = "dfs", pos = (775,200), screen = screen, maze = self.maze, SPEED = speed)
    self.btn_a = ButtonDiscover(alg = "a*", pos = (775,250), screen = screen, maze = self.maze, SPEED = speed)
    self.btn_bfs = ButtonDiscover(alg = "bfs", pos = (775,300), screen = screen, maze = self.maze, SPEED = speed)
    self.btn_show_map = ButtonShowMap(pos = (775,400), screen = screen)
    self.btn_skip = ButtonSkip(pos = (775,500), screen = screen, bot = bot, maze = maze)
    self.list_btn_discover = [self.btn_dfs, self.btn_a, self.btn_bfs]
    self.btn_cancel = ButtonCancel(self.list_btn_discover, pos = (775,450), screen = screen)

  def ShowAndAct(self, x, y):
    if self.state:
      pygame.draw.rect(self.screen, BACKGROUND_COLOR, (700,0,400,1100))
      self.ShowInfo(f'TIME: {self.time}', pos = (775,175), size=20)
      self.ShowInfo('DISCOVER', size = 15, pos = (815, 350))
      pygame.draw.rect(self.screen, COLOR_SHOW_INFO, (770, 197, 181, 150), 2, 5)
      self.btn_dfs.ShowAndAct(x,y, self.bot)
      self.btn_a.ShowAndAct(x,y,self.bot)
      self.btn_bfs.ShowAndAct(x,y,self.bot)
      self.btn_show_map.ShowAndAct(x,y)
      self.btn_skip.ShowAndAct(x, y)
      self.btn_cancel.ShowAndAct(x, y)

  def ClickButtons(self, x, y):
    if self.state:
      self.btn_show_map.click(x,y, self.bot)
      self.btn_dfs.click(x, y, self.bot, self.btn_show_map, self.list_btn_discover, self)
      self.btn_a.click(x, y, self.bot, self.btn_show_map, self.list_btn_discover, self)
      self.btn_bfs.click(x, y, self.bot, self.btn_show_map, self.list_btn_discover, self)
      self.btn_skip.click(x, y, self.list_menu[1], self.btn_show_map, self.bot)
      self.btn_cancel.click(x, y, self.bot)
      return -1, -1
    return x, y

  def ShowInfo(self, Info, pos = (0,0), size=20):
    fnt = pygame.font.Font('freesansbold.ttf', size)
    text = fnt.render(str(Info), True, COLOR_SHOW_INFO)
    self.screen.blit(text, pos)

    