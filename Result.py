import pygame, sys
from pygame.locals import *
from CreateMatrix import *
from p import *


# Gọi mê cung. Nếu muốn thay đổi size và số lượng gạch thì thêm 2 đối số nữa vào. 
# vị trí 1: size, vị trí 2: phân số (0<x<1), vị trí 3: yêu cầu số 0, 1, 2 (nếu index = 0 thì là ma trận cũ, 1 là test 1, 2 là test 2)
# VD: maze = CreateMaze(20,4/5)
maze = CreateMaze(size = 10, index = 0)

# Thông tin mê cung
xs, ys = maze.get_start_point()
xf, yf = maze.get_end_point()
road = maze.path
list_maze = maze.get_list_maze()
n = maze.get_size()
solutions = FindPath(maze)
highest_score, optimal_path, len_of_best, point_of_best = Optimal_result(maze, solutions)

# Màu
color = (255,255,190)
color1 = (255,9,9)
color_start = (100,100,100)
color_end = (255,0,0)

# Thông số cửa sổ
pygame.init()
square = 40
SIZE = square*n
DISPLAYSURF = pygame.display.set_mode((SIZE, SIZE + square))
pygame.display.set_caption('Hello world!')

#Upload image
img = pygame.image.load("/Users/phong/Documents/pog/ITAproject/brick.png")
decrease = 1
brick = pygame.transform.scale(img, (square - 2*decrease, square - 2*decrease))

# Add score
font = pygame.font.Font('freesansbold.ttf', 10)
def write_score(maze, x, y):
  info = maze.get_list_point()[x][y]
  text = font.render(str(info), True, (255,0,0))
  return text

def ShowInfo(Info, size=30):
  fnt = pygame.font.Font('freesansbold.ttf', size)
  text = fnt.render(str(Info), True, (255, 0, 0))
  return text

while True:
  DISPLAYSURF.fill((255, 255, 255))
  for i in range(n):
    for j in range(n):
      if list_maze[i][j] == 1:
        DISPLAYSURF.blit(brick, (i * square + decrease, j * square + decrease))
      if list_maze[i][j] == 0:
        pygame.draw.rect(DISPLAYSURF, color, (i * square + decrease, j * square + decrease, square - 2 * decrease, square - 2 * decrease))

  pygame.draw.rect(DISPLAYSURF, color_start, (xs * square, ys * square, square, square))
  pygame.draw.rect(DISPLAYSURF, color_end, (xf * square, yf * square, square, square))

  for i in range(n):
    for j in range(n):
      if list_maze[i][j] == 0:
        DISPLAYSURF.blit(write_score(maze,i,j), (i * square + decrease, j * square + decrease))

  for x,y in PathConvert(maze, optimal_path):
    pygame.draw.circle(DISPLAYSURF, (0, 0, 255), (x*square + square/2, y*square + square/2), square/4, square//4)
  DISPLAYSURF.blit(ShowInfo(f'The highest score is {int(highest_score)} with {len_of_best} steps and {int(point_of_best)} points', size=15), (square/2, SIZE))

  for event in pygame.event.get():
      if event.type == QUIT:
          pygame.quit()
          sys.exit()
  pygame.display.update()
