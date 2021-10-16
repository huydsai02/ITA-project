import pygame, sys
from pygame.locals import *
from CreateMatrix import *
from p import *


# Gọi ma trận
info_maze = CreateMaze()
road = info_maze[0].path
maze = info_maze[0].matrix
data = (maze, info_maze[1],info_maze[2],info_maze[3],info_maze[4])
n = len(maze)




# Màu
color = (0,0,0)
color1 = (255,9,9)
color_start = (100,100,100)
color_end = (255,0,0)

print(FindPath(data))

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
      if maze[i][j] == 1:
        pygame.draw.rect(DISPLAYSURF, color, (j * square, i * square, square, square))
      if (i,j) in road:
        pygame.draw.rect(DISPLAYSURF, (255,255,0), (j * square, i * square, square, square/10))

  pygame.draw.rect(DISPLAYSURF, color_start, (0, 0, square, square))
  pygame.draw.rect(DISPLAYSURF, color_end, ((n-1) * square, (n-1) * square, square, square))
  
  for event in pygame.event.get():
      if event.type == QUIT:
          pygame.quit()
          sys.exit()
  pygame.display.update()