from Button import Button

class ButtonNewGame(Button):
  def __init__(self, pos = (0,0), color = (255,255,255), font = 20, size = (170,35), screen = None):
    super().__init__("new game" ,  pos, color, font, size, screen)
    # self.show_solution = False
  def click(self,x, y, game):
    super().click(x,y)
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1]:
      game.NewMaze()
      game.InitialState()

class ButtonAgain(Button):
  def __init__(self, pos = (0,0), color = (255,255,255), font = 20, size = (170,35), screen = None):
    super().__init__("again" ,  pos, color, font, size, screen)
    # self.show_solution = False
  def click(self,x, y, game):
    super().click(x,y)
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1]:
      game.InitialState()