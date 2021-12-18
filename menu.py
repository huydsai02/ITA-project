
class Menu(object):
  def __init__(self, list_menu):
    self.list_menu = list_menu
    self.state = False
    self.time = 0

  def TurnOn(self):
    for menu in self.list_menu:
      menu.state = False
    self.state = True