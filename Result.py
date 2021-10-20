import pygame, sys
from pygame.locals import *
from CreateMatrix import *
from random import randint
from p import *

# size lấy vào kích cỡ mê cung với tham số thứ nhất là số ô ngang mê cung, tham số thứ 2 là số ô dọc mê cung
# Bây giờ mê cung sẽ luôn có path và size luôn là 2 số lẻ
width, height = (9, 9)
s = (random.choice(range(1,width - 2,2)),random.choice(range(1,height - 2,2)))
e = (random.choice(range(1,width - 2,2)),random.choice(range(1,height - 2,2)))
maze = Maze(size = (width, height), num_point= 10, start = s, end = e, multi_path = True)

# Thông tin mê cung
xs, ys = maze.get_start_point()
xf, yf = maze.get_end_point()
list_maze = maze.get_list_maze()
size = maze.get_size()
list_point = list_maze

# Tính toán. Nếu muốn tìm đường đi thì calculate = True không thì False
calculate = True

if calculate == True:
  list_point = maze.get_list_point()
  solutions = FindPath(maze)
  highest_score, optimal_path, len_of_best, point_of_best = Optimal_result(maze, solutions)
# print(optimal_path)

###### Màu
color_start = (255, 199, 0)
color_end = (115, 201, 62)
BACKGROUND_COLOR = (55, 155, 255)
color_road = (252, 251, 250)
color_brick = (102, 38, 60)

##### Thông số cửa sổ
pygame.init()
square = 20
SIZE = (square*size[0], square*size[1] + square)
DISPLAYSURF = pygame.display.set_mode((SIZE[0], SIZE[1]))
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

while True:
  fpsClock.tick(FPS)
  DISPLAYSURF.fill(BACKGROUND_COLOR)
  for i in range(size[0]):
    for j in range(size[1]):
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

    for x,y in PathConvert(maze, optimal_path):
      pygame.draw.circle(DISPLAYSURF, (0, 0, 255), (x*square + square/2, y*square + square/2), square/4, square//4)
    DISPLAYSURF.blit(ShowInfo(f'The highest score is {round(highest_score,2)} with {len_of_best} steps and {int(point_of_best)} points', size=15), (square/2, SIZE[1] - square))

  for event in pygame.event.get():
      if event.type == QUIT or (xs,ys) == (xf,yf):
          pygame.quit()
          sys.exit()
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

  pygame.display.update()


