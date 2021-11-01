from Button import *
pygame.init()

class ButtonShowSolution(Button):
  def __init__(self, pos = (0,0), color = (255,255,255), font = 20, size = (170,35), screen = None):
    super().__init__("show solution" ,  pos, color, font, size, screen)
    # self.show_solution = False
  def click(self,x, y, show_map, l=[]):
    super().click(x,y)
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1]:
      self.state = True
      show_map.state = True
  def active(self):
    pass