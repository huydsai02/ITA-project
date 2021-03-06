import pygame
from menu import Menu
from SimpleButtons import ButtonNewGame, ButtonAgain
from ButtonBestPath import ButtonBestPath
from Color import *
from ButtonUCS import ButtonSolve
from ButtonCancel import ButtonCancel
import UCS


class MenuSolve(Menu):
  def __init__(self, bot, maze, screen, speed, list_menu):
    super().__init__(list_menu)
    self.time = 0
    self.bot = bot
    self.maze = maze
    self.screen = screen
    _, _, _, self.full_step, _ = UCS.Optimal_solution(maze, bot.dict_path)
    self.btn_again = ButtonAgain(name = "back", pos = (775,500), screen = self.screen)
    self.btn_new_game = ButtonNewGame(pos = (775,400), screen = self.screen)
    self.list_btn = [None, None, None]
    self.btn_best_path = ButtonBestPath(pos = (775, 300), screen = self.screen, SPEED = speed, list_button = self.list_btn)
    self.btn_ucs = ButtonSolve(maze, alg = "ucs", screen = self.screen, pos = (775, 200), SPEED= 0.01, list_button = self.list_btn)
    self.btn_enumerate = ButtonSolve(maze, alg = "enumerate", screen = self.screen, pos = (775, 250), SPEED= 0.05, list_button = self.list_btn)
    self.list_btn[0] = self.btn_best_path
    self.list_btn[1] = self.btn_ucs
    self.list_btn[2] = self.btn_enumerate
    self.btn_cancel = ButtonCancel(self.list_btn, pos = (775,450), screen = screen)

  def ShowAndAct(self, x, y):
    if self.state:
      pygame.draw.rect(self.screen, BACKGROUND_COLOR, (700,0,400,1100))
      self.ShowInfo(f'TIME: {self.time}', pos = (775,175), size=20)
      self.btn_again.ShowAndAct(x,y)
      self.btn_new_game.ShowAndAct(x,y)
      self.btn_best_path.ShowAndAct(x, y, self.bot)
      self.btn_ucs.ShowAndAct(x, y, self.bot)
      self.btn_enumerate.ShowAndAct(x, y, self.bot)
      self.btn_cancel.ShowAndAct(x, y)
      self.GradeTable()

  def ClickButtons(self, x, y, game):
    if self.state:
      self.btn_new_game.click(x, y, game)
      self.btn_again.click(x, y, game)
      self.btn_best_path.click(x, y, self.bot, self)
      self.btn_ucs.click(x, y, self.maze, self.bot, self)
      self.btn_enumerate.click(x, y, self.maze, self.bot, self)
      self.btn_cancel.click(x, y, self.bot)
      return -1, -1
    return x, y

  def ShowInfo(self, Info, pos = (0,0), size=20):
    fnt = pygame.font.Font('freesansbold.ttf', size)
    text = fnt.render(str(Info), True, COLOR_SHOW_INFO)
    self.screen.blit(text, pos)

  def GradeTable(self):
    self.ShowInfo(f'TOTAL POINT: {self.bot.point}', size=20, pos = (775, 100))
    self.ShowInfo(f'TOTAL STEP: {self.bot.step}', size=20, pos = (775, 125))
    string = f'FINAL POINT: {round(self.bot.point/self.bot.step,2)}' if self.bot.step != 0 else 'FINAL POINT: 0'
    self.ShowInfo(string, size=20, pos = (775, 150)) 