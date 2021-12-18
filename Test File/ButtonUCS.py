from os import curdir
from Button import *
from Color import *
import time
import UCS
import Logic
pygame.init()

class ButtonSolve(Button):
  def __init__(self,maze, alg = 'ucs', pos = (0,0), font = 20, size = (170,45), screen = None, SPEED = 0.07, list_button = None):
    super().__init__(alg ,  pos, font, size, screen)
    self.maze = maze
    self.alg = alg.lower()
    self.initial = 0
    self.speed = SPEED
    self.remember = []
    self.DrawRed = set()
    self.set_add = set()
    self.list_button = list_button
  def click(self,x, y, maze, bot, menu):
    super().click(x,y)
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1] and self.other_state and not self.state:
      self.side = bot.side
      for btn in self.list_button:
        if self.name != btn.name:
          btn.other_state = False
      self.DrawRed = set()
      self.set_add = set()
      self.change_state()
      self.initial = 0
      bot.InitialBot()
      t1 = time.time()
      if self.alg == "ucs":
        bot.point, _, bot.step, menu.full_step, self.step_expand = UCS.Optimal_solution(maze, bot.dict_path)
      elif self.alg == "enumerate":
        bot.point, _, bot.step, menu.full_step, self.step_expand = Logic.Optimal_solution(maze, bot.dict_path)

      menu.time = round(time.time() - t1,3)
      self.remember = bot.PathHasGone
      bot.PathHasGone = []
      bot.point = bot.step = 0

  def ShowBotGo(self, l, i, bot):		
    number = int(i)
    if number < len(l):
      info_extend = l[number]
      current_set = set(info_extend[0])
      bot.point = info_extend[1]
      bot.step = info_extend[2]
      if current_set != self.DrawRed:
        self.set_add = current_set - self.DrawRed
        self.DrawRed = current_set
      bot.draw()
      self.DrawCircle(self.DrawRed, (179, 210, 229), bot)
      self.DrawCircle(self.set_add, (255, 195, 0), bot)
      return True

  def active(self, bot):
    if self.state:
      self.initial += self.speed
      res = self.ShowBotGo(self.step_expand, self.initial, bot)
      if res == None:
        time.sleep(0.5)
        self.DrawCircle(self.DrawRed, (179, 210, 229), bot)
        self.set_add = set()
        for _ in self.list_button:
          _.other_state = True
        self.state = False
        bot.PathHasGone = self.remember

  def ShowAndAct(self, x, y, bot):
    self.show(x,y)
    self.active(bot)
    
  def DrawCircle(self,l, color, bot):
    decrease = 0
    radius = self.side // 3
    side = self.side
    for (x, y) in l:
      pygame.draw.circle(self.screen, color, (x*side + side/2, y*side + side/2), radius-2*decrease)
    bot.write_score()

    
