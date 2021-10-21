import pygame, sys
from pygame.locals import *
from HandleEventFunction import * 
from HandleInfoFunction import * 


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
        self.screen.blit(self.surface, (self.x, self.y))
 
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
SIZE = (700,500)
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

# button1 = Button("Click here", (0, 0), font=30, bg="navy", feedback="Hide", screen = DISPLAYSURF, func = a)
def DrawCircle(l, size, color):
  for (x, y) in l:
    pygame.draw.circle(DISPLAYSURF, color, (x*size + size/2, y*size + size/2), size//4)

while True:
  fpsClock.tick(FPS)
  DISPLAYSURF.fill(BACKGROUND_COLOR)
  # Draw rect
  DrawRectangle(cr, (square, square), color_road)
  DrawRectangle(cb, (square, square), color_brick)
  DrawRectangle([(xs,ys)], (square, square), color_start)
  DrawRectangle([(xf, yf)], (square, square), color_end)
  write_score(maze, cp, (square, square))
  DrawCircle(optimal_path, square, (0, 0, 255))

  DISPLAYSURF.blit(ShowInfo(f'The highest score is {round(highest_score,2)} with {len_of_best} steps and {int(point_of_best)} points', size=15), (square/2, SIZE[1]))
  
  for event in pygame.event.get():
    if event.type == QUIT or (xs,ys) == (xf,yf):
      pygame.quit()
      sys.exit()
    # button1.click(event)
    if event.type == pygame.KEYDOWN:
      if event.key in [K_s, K_DOWN]:
        if (xs,ys+1) in cr:
          xs, ys = NextPosition(xs,ys,(0,1), maze)

      if event.key in [K_w,K_UP]:
        if (xs,ys-1) in cr:
          xs, ys = NextPosition(xs,ys,(0,-1), maze)

      if event.key in [K_a, K_LEFT]:
        if (xs-1,ys) in cr:
          xs, ys = NextPosition(xs,ys,(-1,0), maze)

      if event.key in [K_d, K_RIGHT]:
        if (xs+1,ys) in cr:
          xs, ys = NextPosition(xs,ys,(1,0), maze)
  # button1.show()
  pygame.display.update()


