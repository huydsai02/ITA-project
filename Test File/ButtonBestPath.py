from Button import *
pygame.init()

class ButtonBestPath(Button):

  def __init__(self, name = "run solution", pos = (0,0), font = 20, size = (170,45), screen = None, SPEED = 0.07, list_button = None):
    super().__init__(name ,  pos, font, size, screen)
    self.initial = 0
    self.speed = SPEED
    self.op_road = []
    self.remember = None
    self.list_button = list_button
    self.has_gone = []

  def click(self,x, y, bot, menu):
    super().click(x,y)
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1] and self.other_state and not self.state:
      self.op_road = menu.full_step
      self.remember = bot.PathHasGone
      self.side = bot.side
      self.has_gone = [menu.maze.get_start_point()]
      for btn in self.list_button:
        if self.name != btn.name:
          btn.other_state = False
      self.change_state()
      self.initial = 0
      bot.InitialBot()

  def ShowBotGo(self, l, i):		
    if int(i) < len(l):
      consider = l[int(i)]
      point = consider[0]
      if point not in self.has_gone:
        self.has_gone.append(point)
      return point

  def ShowAndAct(self, x, y, bot):
    self.show(x,y)
    self.active(bot)

  def active(self, bot):
    if self.state:
      self.DrawCircle(self.has_gone, (179, 210, 229), bot)
      self.initial += self.speed
      res = self.ShowBotGo(self.op_road, self.initial)
      if res != None:
        bot.nc = res
      else:
        for _ in self.list_button:
          _.other_state = True
        self.state = False
        bot.PathHasGone = self.remember

  def DrawCircle(self,l, color, bot):
    decrease = 0
    radius = self.side // 3
    side = self.side
    for (x, y) in l:
      pygame.draw.circle(self.screen, color, (x*side + side/2, y*side + side/2), radius-2*decrease)
    bot.write_score()
    
