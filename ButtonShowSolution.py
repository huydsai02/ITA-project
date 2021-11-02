from Button import *
pygame.init()

class ButtonShowSolution(Button):
  COLOR = (150,150,150)
  def __init__(self, pos = (0,0), color = (255,255,255), font = 20, size = (170,35), screen = None):
    super().__init__("show solution" ,  pos, color, font, size, screen)
    self.path = [(2,4)]
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
      self.DrawCircle(self.path, self.COLOR, radius)
      self.bot.write_score()
      self.DrawCircle([self.bot.nc], self.bot.COLOR_START, self.side//2)
      pygame.display.update()
