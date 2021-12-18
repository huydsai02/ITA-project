from Button import Button

class ButtonCancel(Button):
  def __init__(self, list_button, pos = (0,0), font = 20, size = (170,45), screen = None):
    super().__init__("cancel" ,  pos, font, size, screen)
    self.list_button = list_button

  def click(self,x, y, bot):
    super().click(x,y)
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1]:
      for _ in self.list_button:
        _.other_state = True
        _.state = False
      bot.InitialBot()
      bot.draw()