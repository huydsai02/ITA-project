import pygame, sys
from pygame.locals import *
from CreateMatrix import *
from random import randint
from Logic import *

class Button:
    """Create a button, then blit the surface in the while loop"""
 
    def __init__(self, text,  pos, font, screen, bg="black", feedback="", size = (150,50), func = None):
        self.x, self.y = pos
        self.screen = screen
        self.size = size
        self.font = pygame.font.SysFont("Arial", font)
        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, bg)
        self.handle = func
        
 
    def change_text(self, text, bg="black"):
        ### Hàm xử lý khi click vào ###
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        # self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 
    def show(self):
        self.screen.blit(button1.surface, (self.x, self.y))
 
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        print(x,y)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                print(x,y)
                if self.rect.collidepoint(x, y):
                    self.change_text(self.feedback, bg="red")
                    self.handle()

width, height = (30, 30)
s = (random.choice(range(1,width - 2,2)),random.choice(range(1,height - 2,2)))
e = (random.choice(range(1,width - 2,2)),random.choice(range(1,height - 2,2)))
maze = Maze(size = (width, height), num_point= 30, start = s, end = e, multi_path = False)

# Thông tin mê cung
xs, ys = maze.get_start_point()
xf, yf = maze.get_end_point()
list_maze = maze.get_list_maze()
list_point = list_maze
size = maze.get_size()

# Tính toán. Nếu muốn tìm đường đi thì calculate = True không thì False
calculate = False

if calculate == True:
  list_point = maze.get_list_point()
  (score, optimal_path, len_of_best), main_path, list_start = Optimize_solution(maze)

  highest_score = score / len_of_best
  point_of_best = score

###### Màu
color_start = (255, 199, 0)
color_end = (115, 201, 62)
BACKGROUND_COLOR = (55, 155, 255)
color_road = (252, 251, 250)
color_brick = (102, 38, 60)

##### Thông số cửa sổ
pygame.init()
square = 10
SIZE = (square*size[0] + 200, square*size[1] + square)
DISPLAYSURF = pygame.display.set_mode((SIZE[0]+100, SIZE[1]))
pygame.display.set_caption('Maze')

#Upload image
# img = pygame.image.load("./img/brick.png")# replace by ur path
decrease = 0
# brick = pygame.transform.scale(img, (square - 2*decrease, square - 2*decrease))

# Add score
font = pygame.font.Font('freesansbold.ttf', 10)
def write_score(maze, x, y):
  info = maze.get_list_point()[x][y]
  if info != 0:
    s = str(info)
  else:
    s = ""
  text = font.render(s, True, (255,0,0))
  return text

def ShowInfo(Info, size=30):
  fnt = pygame.font.Font('freesansbold.ttf', size)
  text = fnt.render(str(Info), True, (255, 0, 0))
  return text

def NextPosition(x, y, step, l = list_maze, lp = list_point):
  nx = x + step[0]
  ny = y + step[1]

  while not CanTurn(nx, ny) and not LaNgoCut(nx, ny) and lp[nx][ny] == 0 and l[nx][ny] == 0:
    nx += step[0]
    ny += step[1]

  return (nx,ny)

def CanTurn(x, y, l = list_maze):
  check_direction = [[(1,0),(0,1)], [(-1,0),(0,1)], [(1,0),(0,-1)], [(-1,0),(0,-1)]]
  for pair in check_direction:
    count = 0
    for d in pair:
      if l[x + d[0]][y + d[1]] != 1:
        count += 1
    if count == 2:
      return True
  return False

def LaNgoCut(x, y, l = list_maze):
  check_direction = [[(1,0),(0,1),(0,-1)], [(-1,0),(0,1),(0,-1)], [(1,0),(-1,0),(0,-1)], [(-1,0),(1,0),(0,1)]]
  for pair in check_direction:
    count = 0
    for d in pair:
      if l[x + d[0]][y + d[1]] == 1:
        count += 1
    if count == 3:
      return True
  return False

#Set FPS
FPS = 60
fpsClock = pygame.time.Clock()






####### Xử lý button
def a():
  print(1)
button1 = Button("Click here", (0, 0), font=30, bg="navy", feedback="Hide", screen = DISPLAYSURF, func = a)
while True:
  fpsClock.tick(FPS)
  DISPLAYSURF.fill(BACKGROUND_COLOR)
  for i in range(size[0]):
    for j in range(size[1]):
      if calculate:
        if ((i, j) in list_start or (i,j) in main_path) and False:
          continue
      if list_maze[i][j] == 1:
        # DISPLAYSURF.blit(brick, (i * square + decrease, j * square + decrease))
        pygame.draw.rect(DISPLAYSURF, color_brick, (i * square + decrease, j * square + decrease, square - 2 * decrease, square - 2 * decrease))
      if list_maze[i][j] != 1:
        pygame.draw.rect(DISPLAYSURF, color_road, (i * square + decrease, j * square + decrease, square - 2 * decrease, square - 2 * decrease))

  pygame.draw.rect(DISPLAYSURF, color_start, (xs * square, ys * square, square, square))
  pygame.draw.rect(DISPLAYSURF, color_end, (xf * square, yf * square, square, square))

  if calculate == True:
    for i in range(size[0]):
      for j in range(size[1]):
        if list_maze[i][j] == 0:
          DISPLAYSURF.blit(write_score(maze,i,j), (i * square + decrease, j * square + decrease))

    for x,y in optimal_path:
      pygame.draw.circle(DISPLAYSURF, (0, 0, 255), (x*square + square/2, y*square + square/2), square/4, square//4)
    DISPLAYSURF.blit(ShowInfo(f'The highest score is {round(highest_score,2)} with {len_of_best} steps and {int(point_of_best)} points', size=15), (square/2, SIZE[1] - square))

  for event in pygame.event.get():
      if event.type == QUIT or (xs,ys) == (xf,yf):
          pygame.quit()
          sys.exit()
      button1.click(event)
      if event.type == pygame.KEYDOWN:
        if event.key in [K_s, K_DOWN]:
          if list_maze[xs][ys+1] != 1:
            xs, ys = NextPosition(xs,ys,(0,1))

        if event.key in [K_w,K_UP]:
          if list_maze[xs][ys-1] != 1:
            xs, ys = NextPosition(xs,ys,(0,-1))

        if event.key in [K_a, K_LEFT]:
          if list_maze[xs-1][ys] != 1:
            xs, ys = NextPosition(xs,ys,(-1,0))

        if event.key in [K_d, K_RIGHT]:
          if list_maze[xs+1][ys] != 1:
            xs, ys = NextPosition(xs,ys,(1,0))
  button1.show()
  pygame.display.update()


