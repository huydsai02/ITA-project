import pygame, sys
from pygame.locals import *
from CreateMatrix import *
from p import *


# Gọi mê cung và thông tin mê cung
maze = CreateMaze()
xs, ys = maze.get_start_point()
xf, yf = maze.get_end_point()
road = maze.path
list_maze = maze.get_list_maze()
n = maze.n
Solution = FindPath(maze)

print(Solution)

# Màu
color = (0,0,0)
color1 = (255,9,9)
color_start = (100,100,100)
color_end = (255,0,0)


# Thông số cửa sổ
pygame.init()
square = 40
SIZE = square*n
DISPLAYSURF = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption('Hello world!')

while True:
  DISPLAYSURF.fill((255, 255, 255))
  for i in range(n):
    pygame.draw.line(DISPLAYSURF ,color1,(0, i*square),(SIZE,i*square))
  for i in range(n):
    pygame.draw.line(DISPLAYSURF ,color1,(i * square, 0),(i * square,SIZE))
  for i in range(n):
    for j in range(n):
      if list_maze[i][j] == 1:
        pygame.draw.rect(DISPLAYSURF, color, (i * square, j * square, square, square))
      if (i,j) in road:
        pygame.draw.rect(DISPLAYSURF, (255,255,0), (i * square, j * square, square, square/10))
  pygame.draw.rect(DISPLAYSURF, color_start, (xs * square, ys * square, square, square))
  pygame.draw.rect(DISPLAYSURF, color_end, (xf * square, yf * square, square, square))
  for i in [Solution[0]]:
    lst = [(xs, ys)]
    xt, yt = xs, ys
    for j in i:
      if j == 'U':
        yt-=1
      elif j == 'D':
        yt+=1
      elif j == 'R':
        xt+=1
      elif j == 'L':
        xt-=1
      lst.append((xt, yt))
    for (x, y) in lst:
      pygame.draw.circle(DISPLAYSURF, (0, 0, 255), (x*square + square/2, y*square + square/2), square/4, square//4)

  
  for event in pygame.event.get():
      if event.type == QUIT:
          pygame.quit()
          sys.exit()
  pygame.display.update()
