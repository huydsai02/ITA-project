from Button import *
pygame.init()

class ButtonShowMap(Button):
  def __init__(self, pos = (0,0), color = (255,255,255), font = 20, size = (170,35), screen = None):
    super().__init__("full maze" ,  pos, color, font, size, screen)
    # self.seen = False
  def click(self,x, y, bot):
    super().click(x,y)
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1]:
      self.change_state()
      bot.draw()
  def change_state(self):
    ewr = True if self.state == False else False
    self.state = ewr
  def active(self):
    self.name = "full maze" if self.state == False else "around"

    
