from Button import *
pygame.init()

class ButtonBestPath(Button):
  def __init__(self, name = "Best path", pos = (0,0), font = 20, size = (170,35), screen = None, SPEED = 0.07):
    super().__init__(name ,  pos, font, size, screen)
    self.initial = 0
    self.speed = SPEED
    self.op_road = []
    self.optimal_path = []
  def click(self,x, y, bot, solution, show_map, l):
    super().click(x,y)
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1] and self.other_state and not self.state:
      solution.state = False
      show_map.state = False
      self.l = l
      self.side = bot.side
      for btn in l:
        if self.name != btn.name:
          btn.other_state = False
      self.change_state()
      self.initial = 0
      bot.InitialBot()

  def ShowBotGo(self, l, i):		
    if int(i) < len(l):
      consider = l[int(i)]
      point = consider[0]
      return point
  def active(self, bot):
    if self.state:
      self.initial += self.speed
      res = self.ShowBotGo(self.op_road, self.initial)
      if res != None:
        bot.nc = res
      else:
        for _ in self.l:
          _.other_state = True
        self.state = False


    
