import pygame, sys
from pygame.locals import *
from CreateMatrix import *
from random import randint
from p import *

# size lấy vào kích cỡ mê cung với tham số thứ nhất là số ô ngang mê cung, tham số thứ 2 là số ô dọc mê cung
# Bây giờ mê cung sẽ luôn có path và size luôn là 2 số lẻ
maze = Maze(size = (131,65))

# Thông tin mê cung
xs, ys = maze.get_start_point()
xf, yf = maze.get_end_point()
list_maze = maze.get_list_maze()
size = maze.get_size()

# Tính toán. Nếu muốn tìm đường đi thì calculate = True không thì False
calculate = True

if calculate == True:
  solutions = FindPath(maze)
  highest_score, optimal_path, len_of_best, point_of_best = Optimal_result(maze, solutions)
# print(optimal_path)

###### Màu
color_start = (255, 199, 0)
color_end = (115, 201, 62)
BACKGROUND_COLOR = (55, 155, 255)
color_road = (252, 251, 250)
color_brick = (102, 38, 60)

# color_road = (255,255,190)
# color_road = (239, 251, 208)
# color_brick = (35, 91, 5)


##### Thông số cửa sổ
pygame.init()
square = 10
SIZE = (square*size[0], square*size[1] + square)
DISPLAYSURF = pygame.display.set_mode((SIZE[0], SIZE[1]))
pygame.display.set_caption('Hello world!')

#Upload image
img = pygame.image.load("./img/brick.png")# replace by ur path
decrease = 0
brick = pygame.transform.scale(img, (square - 2*decrease, square - 2*decrease))

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

while True:
  DISPLAYSURF.fill(BACKGROUND_COLOR)
  for i in range(size[0]):
    for j in range(size[1]):
      if list_maze[i][j] == 1:
        DISPLAYSURF.blit(brick, (i * square + decrease, j * square + decrease))
        pygame.draw.rect(DISPLAYSURF, color_brick, (i * square + decrease, j * square + decrease, square - 2 * decrease, square - 2 * decrease))
      if list_maze[i][j] == 0:
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
      if event.type == QUIT:
          pygame.quit()
          sys.exit()
  pygame.display.update()


