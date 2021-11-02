import pygame

class Button:
  """Create a button, then blit the surface in the while loop"""
  def __init__(self, name,  pos = (0,0), color = (255,255,255), font = 20, size = (170,35), screen = None):
    self.font = pygame.font.SysFont("Arial", font)
    self.size = size
    self.pos = pos
    self.color = color
    self.name = name
    self.full_coor = self.get_full_coor()
    self.screen = screen
    self.state = False
    self.other_state = True

  def show(self, q, w):
    self.hover(q,w)
    self.draw()
    
  def draw(self):
    screen = self.screen
    x, y = self.pos
    i,j = self.size
    text = self.font.render(self.name.upper(), True, (0,0,0))
    text_size = text.get_size()
    k = (i - text_size[0]) // 2
    h = (j - text_size[1]) // 2
    de = 2
    pygame.draw.rect(screen, (255,0,0), (x, y, i, j))
    pygame.draw.rect(screen, self.color, (x + de, y + de, i - 2*de, j - 2*de))
    screen.blit(text, (x + k, y + h))
    pygame.display.update()

  def get_full_coor(self):
    x, y = self.pos
    i, j = self.size
    h = x + i
    k = y + j
    self.full_coor = [(x,h),(y,k)]
    return self.full_coor

  def hover(self, x, y):
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1]:
      self.color = (200,200,200)
    else:
      self.color = (255,255,255)
  
  def click(self, x, y):
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1]:
      self.color = (255,0,0)
    else:
      self.color = (255,255,255)
    self.draw()

  def TurnOnOffOtherState(self, l):
    for _ in l:
      _.other_state = False if _.other_state == True else True
  
  def get_state(self):
    return self.state
  
  def change_state(self):
    ewr = True if self.state == False else False
    self.state = ewr