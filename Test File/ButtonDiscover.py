from Button import *
from Color import *
import time
########################## m muốn so sánh code của m với file nào thì sửa ở cái chữ import dưới. muốn so sánh 
# file logic với file A thì để là import A as t, muốn với file B thì để là import B as t
import GeneralFunction
pygame.init()

class ButtonDiscover(Button):

  def __init__(self, maze, alg = 'dfs', pos = (0,0), font = 20, size = (170,45), screen = None, SPEED = 0.07):
    super().__init__(alg ,  pos, font, size, screen)
    self.maze = maze
    self.alg = alg.lower()
    self.initial = 0
    self.speed = SPEED
    self.path_bot_go = None

  def click(self,x, y, bot, show_map, list_button_discover, menu):
    super().click(x,y)
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1] and self.other_state and not self.state:
      show_map.state = False
      self.l = list_button_discover
      self.side = bot.side
      for btn in list_button_discover:
        if self.name != btn.name:
          btn.other_state = False
      self.initial = 0
      self.change_state()
      bot.InitialBot()
      size = self.maze.get_size()
      end_point = self.maze.get_end_point()
      list_point = self.maze.get_list_point()
      list_consider = [(i, j) for i in range(size[0]) for j in range(size[1]) if list_point[i][j] != 0 or (i,j) == end_point]
      t1 = time.time()
      bot.dict_path, self.path_bot_go = GeneralFunction.DiscoverMaze(self.maze, list_consider, self.alg)
      menu.time = round(time.time() - t1, 3)

  def ShowBotGo(self, l, i):		
    if int(i) < len(l):
      consider = l[int(i)]
      point = consider[0]
      dims = consider[1]
      res = [] 
      if dims != [] and dims[0] != ():    
        for a,b in dims:
          j = point[0] + a
          k = point[1] + b
          res.append((j,k))
        self.DrawCircle(res, COLOR_DIMENSION)
      return point

  def active(self, bot):
    if self.state:
      self.initial += self.speed
      res = self.ShowBotGo(self.path_bot_go, self.initial)
      if res != None:
        bot.nc = res
      else:
        for _ in self.l:
          _.other_state = True
        self.state = False

  def ShowAndAct(self, x, y, bot):
    self.show(x,y)
    self.active(bot)
    
  def DrawCircle(self,l, color):
    decrease = 0
    radius = self.side // 5
    side = self.side
    for (x, y) in l:
      pygame.draw.circle(self.screen, color, (x*side + side/2, y*side + side/2), radius-2*decrease)

    
