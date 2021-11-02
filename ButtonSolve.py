from Button import *
from Color import *
import Logic
pygame.init()

class ButtonSolve(Button):

  def __init__(self,maze, alg = 'dfs', pos = (0,0), font = 20, size = (170,35), screen = None, solution = None, best_path = None, SPEED = 0.07):
    super().__init__(alg ,  pos, font, size, screen)
    self.maze = maze
    self.alg = alg.lower()
    self.initial = 0
    self.speed = SPEED
    if alg == "dfs":
        self.score, self.optimal_path, self.len_of_best, self.op_road, self.path_bot_go,\
             self.main_path = Logic.Optimize_solution(maze, alg)
        solution.path = self.optimal_path
        solution.point = self.score
        solution.length = self.len_of_best
        best_path.op_road = self.op_road
        best_path.optimal_path = self.optimal_path       
    else: 
        self.score = self.optimal_path = self.len_of_best = self.op_road = self.path_bot_go = self.main_path = None
  def click(self,x, y, bot, solution, show_map, l, best_path):
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
      if self.score == None:
        self.score, self.optimal_path, self.len_of_best, self.op_road, self.path_bot_go\
            , self.main_path = Logic.Optimize_solution(self.maze, self.alg)
      solution.path = self.optimal_path
      solution.point = self.score
      solution.length = self.len_of_best
      best_path.op_road = self.op_road
      best_path.optimal_path = self.optimal_path         


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

  def DrawCircle(self,l, color):
    decrease = 0
    radius = self.side // 5
    side = self.side
    for (x, y) in l:
      pygame.draw.circle(self.screen, color, (x*side + side/2, y*side + side/2), radius-2*decrease)

    