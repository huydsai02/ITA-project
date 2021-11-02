from Button import *
pygame.init()

class ButtonShowSolution(Button):
  COLOR = (200,200,200)
  COLOR_BRICK = (102, 38, 60)
  COLOR_ROAD = (252, 251, 250)
  COLOR_START = (255, 199, 0)
  COLOR_END = (115, 201, 62)
  BACKGROUND_COLOR = (55, 155, 255)
  SEED_COLOR = (0,0,0)
  def __init__(self, pos = (0,0), color = (255,255,255), font = 20, size = (170,35), screen = None, maze = None):
    super().__init__("show solution" ,  pos, color, font, size, screen)
    self.path = [(2,4)]
    self.maze = maze
    self.lr, self.lb = self.maze.TakeCoordinateRoad()		
    self.lp = self.maze.TakeCoordinatePoint()
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
      lr, lb, lp = self.lr, self.lb, self.lp
      self.decrease = 0
      self.DrawRectangle(lr, self.COLOR_ROAD)
      self.DrawRectangle(lb, self.COLOR_BRICK)
      self.DrawCircle(self.path, self.COLOR, radius)
      self.bot.write_score()
      self.bot.step = self.length
      self.bot.point = self.point
      self.DrawCircle([self.maze.get_end_point()], self.COLOR_END,self.side//2)
      self.DrawCircle([self.bot.nc], self.bot.COLOR_START, self.side//2)
      pygame.display.update()

  def DrawRectangle(self, l, color):
    decrease = self.decrease
    side = self.side
    for (i, j) in l:
      pygame.draw.rect(self.screen, color, (i * side + decrease, j * side + decrease, side - 2 * decrease, side - 2 * decrease))
