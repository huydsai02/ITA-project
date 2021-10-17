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
n = maze.get_size()
Solution = FindPath(maze)
All_Path = FindCoordinatePath(maze, Solution)
highest_score, optimal_path = Optimal_result(maze, All_Path)

# Màu
color = (255,255,190)
color1 = (255,9,9)
color_start = (100,100,100)
color_end = (255,0,0)

# Thông số cửa sổ
pygame.init()
square = 40
SIZE = square*n
DISPLAYSURF = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption('Hello world!')

#Upload image
img = pygame.image.load("./img/brick.png")
decrease = 1
brick = pygame.transform.scale(img, (square - 2*decrease, square - 2*decrease))

# Add score
font = pygame.font.Font('freesansbold.ttf', 10)
def write_score(maze, x, y):
  info = maze.get_list_point()[x][y]
  text = font.render(str(info), True, (255,0,0))
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

  for x,y in optimal_path:
    pygame.draw.circle(DISPLAYSURF, (0, 0, 255), (x*square + square/2, y*square + square/2), square/4, square//4)
  for i in range(n):
    for j in range(n):
      if list_maze[i][j] == 0:
        DISPLAYSURF.blit(write_score(maze,i,j), (i * square + decrease, j * square + decrease))
  for event in pygame.event.get():
      if event.type == QUIT:
          pygame.quit()
          sys.exit()
  pygame.display.update()
