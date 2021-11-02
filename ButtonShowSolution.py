from Button import *
from Color import *
pygame.init()

class ButtonShowSolution(Button):
  def __init__(self, pos = (0,0), font = 20, size = (170,45), screen = None):
    super().__init__("show solution" ,  pos, font, size, screen)
    self.path = [(2,4)]
    self.length = 0
    self.point = 0
  def click(self,x, y, show_map, bot):
    super().click(x,y)
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1] and self.other_state:
      self.bot = bot
      bot.InitialBot()
      self.state = True
      show_map.state = True
      # show_map.other_state = False
      self.decrease = bot.decrease
      self.side = bot.side
      bot.draw()
  def DrawCircle(self,l, color, radius):
    decrease = 0
    side = self.side
    for (x, y) in l:
      pygame.draw.circle(self.screen, color, (x*side + side/2, y*side + side/2), radius-2*decrease)
    
  def active(self):
    if self.state:
      radius = self.side // 3
      self.bot.step = self.length
      self.bot.point = self.point
      self.bot.draw()
      self.DrawCircle(self.path, COLOR_GUIDE, radius)
      self.bot.write_score()
      self.DrawCircle([self.bot.maze.get_end_point()], COLOR_END,self.side//2)
      self.DrawCircle([self.bot.nc], COLOR_START, self.side//2)

