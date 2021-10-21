import pygame, sys
from pygame.locals import *
from HandleEventFunction import * 
from HandleInfoFunction import * 


class Button:
  """Create a button, then blit the surface in the while loop"""
  def __init__(self, name,  pos = (0,0), color = (255,255,255), font = 30, size = (150,50)):
    self.font = pygame.font.SysFont("Arial", font)
    self.size = size
    self.pos = pos
    self.color = color
    self.name = name
    self.full_coor = self.get_full_coor()

  def show(self, q, w):
    x, y = self.pos
    i,j = self.size
    text = self.font.render(self.name, True, (0,0,0))
    text_size = text.get_size()
    k = (i - text_size[0]) // 2
    h = (j - text_size[1]) // 2
    de = 2
    self.hieu_ung(q,w)
    pygame.draw.rect(DISPLAYSURF, (255,0,0), (x, y, i, j))
    pygame.draw.rect(DISPLAYSURF, self.color, (x + de, y + de, i - 2*de, j - 2*de))
    DISPLAYSURF.blit(text, (x + k, y + h))

  def get_full_coor(self):
    x, y = self.pos
    i, j = self.size
    h = x + i
    k = y + j
    self.full_coor = [(x,h),(y,k)]
    return self.full_coor

  def hieu_ung(self, x, y):
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1]:
      self.color = (200,200,200)
    else:
      self.color = (255,255,255)


###### All need info 
maze, cp, cr, cb, score, optimal_path, len_of_best, highest_score, point_of_best = AllNeedInfo()
xs, ys = maze.get_start_point(); xf, yf = maze.get_end_point()

###### Màu
color_start = (255, 199, 0)
color_end = (115, 201, 62)
BACKGROUND_COLOR = (55, 155, 255)
color_road = (252, 251, 250)
color_brick = (102, 38, 60)

##### Thông số cửa sổ
pygame.init()
SIZE = (900,600)
square = min(SIZE) // max(maze.get_size())
DISPLAYSURF = pygame.display.set_mode((SIZE[0], SIZE[1] + square))
pygame.display.set_caption('Maze')
FPS = 60
fpsClock = pygame.time.Clock()
decrease = 0

#Upload image
# img = pygame.image.load("./img/brick.png")# replace by ur path
# brick = pygame.transform.scale(img, (square - 2*decrease, square - 2*decrease))

def write_score(maze, l, size):
  a, b = size
  font = pygame.font.Font('freesansbold.ttf', 10)
  lp = maze.get_list_point()
  for i, j in l:
    text = font.render(str(lp[i][j]), True, (255,0,0))
    DISPLAYSURF.blit(text, (i * a + decrease, j * b + decrease))

def ShowInfo(Info, size=30):
  fnt = pygame.font.Font('freesansbold.ttf', size)
  text = fnt.render(str(Info), True, (255, 0, 0))
  return text

def DrawRectangle(l, size, color):
  a, b = size
  for (i, j) in l:
    pygame.draw.rect(DISPLAYSURF, color, (i * a + decrease, j * b + decrease, a - 2 * decrease, b - 2 * decrease))

def DrawCircle(l, size, color):
  for (x, y) in l:
    pygame.draw.circle(DISPLAYSURF, color, (x*size + size/2, y*size + size/2), size//4)

# Các nút trong chương trình
seen = False
btn_seen = Button(name = "FULL MAZE", pos = (650,50), size = (230, 50))
btn_not_seen = Button(name = "AROUND", pos = (650,50), size = (230, 50))

show_solution = False
btn_show_solution = Button(name = "Show solution", pos = (650,150), size = (230, 50))
while True:
  x, y = pygame.mouse.get_pos()
  fpsClock.tick(FPS)
  DISPLAYSURF.fill(BACKGROUND_COLOR)
  # Draw rect
  DrawRectangle(cr, (square, square), color_road)
  DrawRectangle(cb, (square, square), color_brick)
  DrawRectangle([(xs,ys)], (square, square), color_start)
  DrawRectangle([(xf, yf)], (square, square), color_end)
  write_score(maze, cp, (square, square))
  if show_solution:
    DrawCircle(optimal_path, square, (0, 0, 255))
  if seen == True:
    FullMaze(DrawRectangle,(cr, (square, square), color_road), xs, ys, maze)
  DISPLAYSURF.blit(ShowInfo(f'The highest score is {round(highest_score,2)} with {len_of_best} steps and {int(point_of_best)} points', size=15), (square/2, SIZE[1]))
  
  for event in pygame.event.get():
    if event.type == QUIT or (xs,ys) == (xf,yf):
      pygame.quit()
      sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      a, b = btn_seen.get_full_coor()
      if a[0] <= x <= a[1] and b[0] <= y <= b[1]:
        ewr = True if seen == False else False
        seen = ewr
      a, b = btn_show_solution.get_full_coor()
      if a[0] <= x <= a[1] and b[0] <= y <= b[1]:
        show_solution = True
        seen = False
    if event.type == pygame.KEYDOWN:
      if event.key in [K_s, K_DOWN]:
        if (xs,ys+1) in cr:
          # xs, ys = NextPosition(xs,ys,(0,1), maze)
          ys += 1

      if event.key in [K_w,K_UP]:
        if (xs,ys-1) in cr:
          # xs, ys = NextPosition(xs,ys,(0,-1), maze)
          ys -= 1

      if event.key in [K_a, K_LEFT]:
        if (xs-1,ys) in cr:
          # xs, ys = NextPosition(xs,ys,(-1,0), maze)
          xs -= 1

      if event.key in [K_d, K_RIGHT]:
        if (xs+1,ys) in cr:
          # xs, ys = NextPosition(xs,ys,(1,0), maze)
          xs += 1
  if seen == False:
    btn_seen.show(x,y)
  else:
    btn_not_seen.show(x,y)
  btn_show_solution.show(x,y)
  pygame.display.update()


