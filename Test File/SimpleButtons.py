from Button import *
pygame.init()
class ButtonShowMap(Button):
  def __init__(self, pos = (0,0), font = 20, size = (170,45), screen = None):
    super().__init__("full maze" ,  pos, font, size, screen)
    # self.seen = False
  def click(self,x, y, bot):
    super().click(x,y)
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1]:
      self.change_state()
      bot.draw()
  def active(self):
    self.name = "full maze" if self.state == False else "hide maze"
class ButtonNewGame(Button):
  def __init__(self, pos = (0,0), font = 20, size = (170,45), screen = None):
    super().__init__("new maze" ,  pos, font, size, screen)
    # self.show_solution = False
  def click(self,x, y, game):
    super().click(x,y)
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1]:
      # print("-"*100)
      game.NewMaze()
      game.InitialState()
class ButtonAgain(Button):
  def __init__(self, pos = (0,0), font = 20, size = (170,45), screen = None):
    super().__init__("reset" ,  pos, font, size, screen)
    # self.show_solution = False
  def click(self,x, y, game):
    super().click(x,y)
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1]:
      game.InitialState()


    
