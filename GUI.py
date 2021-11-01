import pygame, sys
from pygame.locals import *
from CreateMatrix import Maze
from Bot import Bot
from ButtonShowMap import ButtonShowMap
from ButtonShowSolution import ButtonShowSolution


class Game(object):
	BACKGROUND_COLOR = (55, 155, 255)
	SIZE = (1050,670)
	COLOR_TEST = (0,0,0)

	def __init__(self):
		_size = (41,41); _num_point = 20; _start = (1,1); _end = (39,39)
		self.maze = Maze(size = _size, num_point = _num_point, start = _start, end = _end)
		pygame.init()
		self.DISPLAYSURF = pygame.display.set_mode((self.SIZE[0], self.SIZE[1]))
		pygame.display.set_caption('Maze')
		self.DISPLAYSURF.fill(self.BACKGROUND_COLOR)
		self.CreateButton()
		self.bot = Bot(self.maze, self.btn_show_map, self.DISPLAYSURF, self.SIZE)

	def CreateButton(self):
		self.btn_show_map = ButtonShowMap(pos = (775,200), screen = self.DISPLAYSURF)
	def run(self):
		FPS = 60
		fpsClock = pygame.time.Clock()
		while True:
			fpsClock.tick(FPS)
			x, y = pygame.mouse.get_pos()
			self.bot.draw()
			self.bot.CountAndRemember()
			self.btn_show_map.show(x,y)
			self.btn_show_map.active()
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.btn_show_map.click(x,y)
				if event.type == pygame.KEYDOWN:
					if event.key in [K_s, K_DOWN]:
						self.bot.MoveDown()
					if event.key in [K_w,K_UP]:
						self.bot.MoveUp()
					if event.key in [K_a, K_LEFT]:
						self.bot.MoveLeft()
					if event.key in [K_d, K_RIGHT]:
						self.bot.MoveRight()
	
			

if __name__ == "__main__":
	game = Game()
	game.run()			


