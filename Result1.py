import pygame, sys
from pygame.locals import *
from HandleEventFunction import * 
from HandleInfoFunction import * 

_size = (41,41); _num_point = 20; _start = (1,1); _end = (39,39)
###### All need info 


def init():
  global maze, cp, cr, cb, score, optimal_path, len_of_best, highest_score, point_of_best, path_bot_go, main_path, op_road
  global size, list_point, state, speed, initial, length, seen, show_solution, show_bot_go, one_times, change_when_run
  global list_gone, current_score, total_step, best_path, length1, xs, ys, xf, yf, new_game
  maze, cp1, cr, cb, score, optimal_path, len_of_best, highest_score, point_of_best, path_bot_go, main_path, op_road = \
    AllNeedInfo(size = _size, num_point = _num_point, start = _start, end = _end, alg= 'bfs')
  cp = cp1[:]
  xs, ys = maze.get_start_point(); xf, yf = maze.get_end_point()
  size = maze.get_size()
  list_point = [maze.get_list_point()[i][:] for i in range(len(maze.get_list_point()))]
  translate = {(0,1):"D",(1,0):"R",(0,-1):"U",(-1,0):"L",():""}
  direc = "".join([translate[_[1][0]] for _ in op_road])
  print(direc)
  state = True
  speed = 0.5
  initial = 0
  length = len(path_bot_go)
  seen = False
  show_solution = False
  show_bot_go = False
  one_times = True
  change_when_run = False
  list_gone = []
  current_score = 0
  total_step = 0 
  best_path = False
  length1 = len(op_road)
  new_game = False

init()
class Button:
  """Create a button, then blit the surface in the while loop"""
  def __init__(self, name,  pos = (0,0), color = (255,255,255), font = 20, size = (170,35)):
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
SIZE = (1050,670)
square = min(SIZE) // max(maze.get_size())
DISPLAYSURF = pygame.display.set_mode((SIZE[0], SIZE[1]))
pygame.display.set_caption('Maze')
FPS = 60
fpsClock = pygame.time.Clock()
decrease = 0

#Upload image
# img = pygame.image.load("./img/brick.png")# replace by ur path
# brick = pygame.transform.scale(img, (square - 2*decrease, square - 2*decrease))

def write_score(list_point, l, size):
  a, b = size
  font = pygame.font.Font('freesansbold.ttf', a // 2)
  lp = list_point
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
btn_new_game = Button(name = "new game", pos = (775,150))
btn_seen = Button(name = "FULL MAZE", pos = (775,200))
btn_not_seen = Button(name = "AROUND", pos = (775,200))
btn_show_solution = Button(name = "Show solution", pos = (775,250))
btn_show_bot = Button(name = "EXPLAIN", pos = (775,300))
btn_best_path = Button(name = "BEST PATH", pos = (775,350))
while True:
  old_coor = (xs, ys)
  if int(initial) < length:
    initial += speed
  x, y = pygame.mouse.get_pos()
  fpsClock.tick(FPS)
  DISPLAYSURF.fill(BACKGROUND_COLOR)
  # Draw rect
  # decrease = 1
  DrawRectangle(cr, (square, square), color_road)
  DrawRectangle(cb, (square, square), color_brick)
  current_score += list_point[xs][ys]
  # cp = DelElementFromList((xs,ys), cp)
  list_point[xs][ys] = 0
  if seen == False:
    FullMaze(DrawRectangle,(cr, (square, square), color_road), xs, ys, maze)
  # r, (square, square), color_road, color_brick
  list_gone = PathHasGone(list_gone, cr, cb, DrawRectangle, (cr, (square, square), color_road, color_brick), (xs, ys))
  DrawCircle([(xs, ys)], square, color_start, square//2)
  DrawCircle([(xf, yf)], square, color_end, square//2)
  if show_solution:
    DrawCircle(optimal_path, square, (225, 225, 225), square/3)
    write_score(list_point, cp, (square, square))
    
  if show_bot_go:
    if int(initial) == length - 1:
      state = True
      show_bot_go = False
      one_times = True
      change_when_run = False
    # DrawCircle([(xs, ys)], square, color_start, square//2)    
    res = ShowBotGo(DrawCircle,(cr, square, (0,0,255), square//4), path_bot_go, initial)
    if res != None:    
      xs, ys = res

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
  
  # if show_solution or one_times == False:
  #   DISPLAYSURF.blit(ShowInfo(f'The highest score is {round(highest_score,2)} with {len_of_best} steps and {int(point_of_best)} points'.upper(), size=square), (square/2, SIZE[1]))

  # pos = (650,250), size = (230, 50)
  DISPLAYSURF.blit(ShowInfo(f'TOTAL POINT: {current_score}', size=square), (800, 25))
  DISPLAYSURF.blit(ShowInfo(f'TOTAL STEP: {total_step}', size=square), (800, 50))
  stri = f'FINAL POINT: {round(current_score/total_step,2)}' if total_step != 0 else 'FINAL POINT: 0'
  DISPLAYSURF.blit(ShowInfo(stri, size=square), (800, 75))
    
  for event in pygame.event.get():
    if event.type == QUIT:
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
        list_point = [maze.get_list_point()[i][:] for i in range(len(maze.get_list_point()))]
        total_step = len_of_best
        current_score = point_of_best
        if (xs, ys) != maze.get_start_point():
          total_step -= 1
        xs, ys = maze.get_start_point()
      a, b = btn_show_bot.get_full_coor()
      if a[0] <= x <= a[1] and b[0] <= y <= b[1] and one_times:
        initial = 0
        seen = False
        state = False
        show_bot_go = True
        list_point = [maze.get_list_point()[i][:] for i in range(len(maze.get_list_point()))]
        total_step = 0 if (xs, ys) == maze.get_start_point() else -1
        current_score = 0
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
        total_step = 0 if (xs, ys) == maze.get_start_point() else -1
        current_score = 0
        list_point = [maze.get_list_point()[i][:] for i in range(len(maze.get_list_point()))]
        xs, ys = maze.get_start_point()
        one_times = False
        list_gone = []
        show_solution = True
        change_when_run = True

      a, b = btn_new_game.get_full_coor()
      if a[0] <= x <= a[1] and b[0] <= y <= b[1]:
        init()
        old_coor = (xs,ys)
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
  btn_new_game.show(x,y)
  if seen == False:
    h = cp 
    DrawRectangle(h, (square, square), color_end)
    decrease = 1
    DrawCircle([(xf, yf)], square, color_end, square//2)
  write_score(list_point, cp, (square, square))
  new_coor = (xs, ys)
  if new_coor != old_coor:
    total_step += 1
  pygame.display.update()


