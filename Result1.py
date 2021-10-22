import pygame, sys
from pygame.locals import *
from HandleEventFunction import * 
from HandleInfoFunction import * 
import random

nghich = False
###### All need info 
maze, cp1, cr, cb, score, optimal_path, len_of_best, highest_score, point_of_best, path_bot_go, main_path, op_road = AllNeedInfo(size = (29,29), num_point = 10, start = (1,1), end = (27,27), multi_path = False)
cp = cp1[:]
xs, ys = maze.get_start_point(); xf, yf = maze.get_end_point()
list_point = maze.get_list_point()
size = maze.get_size()
cho = min(size) // 2

khoc = [(i,j) for i in range(size[0]) for j in range(size[1]) if (i,j) not in main_path and maze.get_list_maze()[i][j] != 1]
cay = random.sample(khoc, cho)
# print(cay)
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
    text = self.font.render(self.name.upper(), True, (0,0,0))
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

###### Màu
color_start = (255, 199, 0)
color_end = (115, 201, 62)
BACKGROUND_COLOR = (55, 155, 255)
color_road = (252, 251, 250)
color_brick = (102, 38, 60)

##### Thông số cửa sổ
pygame.init()
SIZE = (950,600)
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
  font = pygame.font.Font('freesansbold.ttf', a // 2)
  lp = maze.get_list_point()
  for i, j in l:
    text = font.render(str(lp[i][j]), True, (255,0,0))
    text_size = text.get_size()
    x = (a - text_size[0]) // 2
    y = (b - text_size[1]) // 2
    DISPLAYSURF.blit(text, (x + i * a + decrease, y + j * b + decrease))

def ShowInfo(Info, size=30):
  fnt = pygame.font.Font('freesansbold.ttf', size)
  text = fnt.render(str(Info), True, (255, 0, 0))
  return text

def DrawRectangle(l, size, color):
  a, b = size
  for (i, j) in l:
    pygame.draw.rect(DISPLAYSURF, color, (i * a + decrease, j * b + decrease, a - 2 * decrease, b - 2 * decrease))

def DrawCircle(l, size, color, radius):
  for (x, y) in l:
    pygame.draw.circle(DISPLAYSURF, color, (x*size + size/2, y*size + size/2), radius-2*decrease)

# Các nút trong chương trình
state = True
speed = 0.07
initial = 0
length = len(path_bot_go)
seen = False
btn_seen = Button(name = "FULL MAZE", pos = (650,50), size = (230, 50))
btn_not_seen = Button(name = "AROUND", pos = (650,50), size = (230, 50))

show_solution = False
btn_show_solution = Button(name = "Show solution", pos = (650,150), size = (230, 50))

show_bot_go = False
one_times = True
change_when_run = False
btn_show_bot = Button(name = "EXPLAIN", pos = (650,250), size = (230, 50))
list_gone = []
current_score = 0
total_step = 0

btn_best_path = Button(name = "BEST PATH", pos = (650,0), size = (230, 30))
best_path = False
length1 = len(op_road)
while True:
  if (xs, ys) in cay and nghich:
    cay = random.sample(khoc, cho)
    xs, ys = maze.get_start_point()

  old_coor = (xs, ys)
  if int(initial) < length:
    initial += speed
  x, y = pygame.mouse.get_pos()
  fpsClock.tick(FPS)
  DISPLAYSURF.fill(BACKGROUND_COLOR)
  # Draw rect
  DrawRectangle(cr, (square, square), color_road)
  DrawRectangle(cb, (square, square), color_brick)

  current_score += list_point[xs][ys]
  list_point[xs][ys] = 0
  if seen == False:
    FullMaze(DrawRectangle,(cr, (square, square), color_road), xs, ys, maze)
  # r, (square, square), color_road, color_brick
  if not nghich:
    list_gone = PathHasGone(list_gone, cr, cb, DrawRectangle, (cr, (square, square), color_road, color_brick), (xs, ys))
  DrawCircle([(xs, ys)], square, color_start, square//2)
  DrawCircle([(xf, yf)], square, color_end, square//2)
  if show_solution:
    DrawCircle(optimal_path, square, (220, 220, 220), square//4)
    write_score(maze, cp, (square, square))
    
  if show_bot_go:
    if int(initial) == length - 1:
      state = True
      show_bot_go = False
      one_times = True
      change_when_run = False
    # DrawCircle([(xs, ys)], square, color_start, square//2)    
    xs, ys = ShowBotGo(DrawCircle,(cr, square, (0,0,255), square//4), path_bot_go, initial)

  if best_path:
    if int(initial) >= length1 - 1:
      state = True
      best_path = False
      one_times = True
      change_when_run = False
    # DrawCircle([(xs, ys)], square, color_start, square//2)
    res = ShowBotGo(DrawCircle,(cr, square, (0,0,255), square//4), op_road, initial)
    if res != None:    
      xs, ys = res
  
  if show_solution or one_times == False:
    DISPLAYSURF.blit(ShowInfo(f'The highest score is {round(highest_score,2)} with {len_of_best} steps and {int(point_of_best)} points'.upper(), size=15), (square/2, SIZE[1]))

  # pos = (650,250), size = (230, 50)
  DISPLAYSURF.blit(ShowInfo(f'TOTAL POINT: {current_score}', size=30), (650, 350))
  DISPLAYSURF.blit(ShowInfo(f'TOTAL STEP: {total_step}', size=30), (650, 450))
  stri = f'FINAL POINT: {round(current_score/total_step,2)}' if total_step != 0 else 'FINAL POINT: 0'
  DISPLAYSURF.blit(ShowInfo(stri, size=30), (650, 550))
    
  for event in pygame.event.get():
    if event.type == QUIT or ((xs, ys) == (xf, yf) and nghich):
      pygame.quit()
      sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
      a, b = btn_seen.get_full_coor()
      if a[0] <= x <= a[1] and b[0] <= y <= b[1] and (state or change_when_run):
        ewr = True if seen == False else False
        seen = ewr
      a, b = btn_show_solution.get_full_coor()
      if a[0] <= x <= a[1] and b[0] <= y <= b[1] and state:
        show_solution = True
        seen = True
        state = False
        if (xs, ys) != maze.get_start_point():
          total_step -= 1
        xs, ys = maze.get_start_point()
      a, b = btn_show_bot.get_full_coor()
      if a[0] <= x <= a[1] and b[0] <= y <= b[1] and one_times:
        initial = 0
        seen = False
        state = False
        show_bot_go = True
        total_step = 0 if (xs, ys) == maze.get_start_point() or total_step != 0 else -1
        total_point = 0
        xs, ys = maze.get_start_point()
        one_times = False
        list_gone = []
        show_solution = False
        change_when_run = True

      a, b = btn_best_path.get_full_coor()
      if a[0] <= x <= a[1] and b[0] <= y <= b[1] and one_times:
        initial = 0
        seen = False
        state = False
        best_path = True
        total_step = 0 if (xs, ys) == maze.get_start_point() or total_step != 0 else -1
        total_point = 0
        xs, ys = maze.get_start_point()
        one_times = False
        list_gone = []
        # show_solution = False
        change_when_run = True

    if event.type == pygame.KEYDOWN:
      if event.key in [K_s, K_DOWN] and state:
        if (xs,ys+1) in cr:
          # xs, ys = NextPosition(xs,ys,(0,1), maze)
          ys += 1

      if event.key in [K_w,K_UP] and state:
        if (xs,ys-1) in cr:
          # xs, ys = NextPosition(xs,ys,(0,-1), maze)
          ys -= 1

      if event.key in [K_a, K_LEFT] and state:
        if (xs-1,ys) in cr:
          # xs, ys = NextPosition(xs,ys,(-1,0), maze)
          xs -= 1

      if event.key in [K_d, K_RIGHT] and state:
        if (xs+1,ys) in cr:
          # xs, ys = NextPosition(xs,ys,(1,0), maze)
          xs += 1
  if seen == False:
    btn_seen.show(x,y)
  else:
    btn_not_seen.show(x,y)
    decrease = 0
  btn_show_solution.show(x,y)
  btn_show_bot.show(x,y)
  btn_best_path.show(x,y)
  cp = DelElementFromList((xs,ys), cp)
  if seen == False:
    h = cp 
    DrawRectangle(h, (square, square), color_end)
    decrease = 1
    DrawCircle([(xf, yf)], square, color_end, square//2)
  write_score(maze, cp, (square, square))
  new_coor = (xs, ys)
  if new_coor != old_coor:
    total_step += 1
  pygame.display.update()


