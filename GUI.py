import pygame, sys
from pygame.locals import *
from CreateMatrix import Maze
from Bot import Bot
from Color import *
from menudiscover import MenuDiscover
from menusolve import MenuSolve

class Game(object):
	SPEED = 1
	_size = (41,41); _num_point = 20; _start = (1,1); _end = (39,39)
	SIZE = (1050,670)

	def __init__(self):
		pygame.init()
		self.DISPLAYSURF = pygame.display.set_mode((self.SIZE[0], self.SIZE[1]))
		pygame.display.set_caption('Maze')
		self.DISPLAYSURF.fill(BACKGROUND_COLOR)
		self.NewMaze()
		self.InitialState()		
	
	def NewMaze(self):
		self.maze = Maze(size = self._size, num_point = self._num_point, start = self._start, end = self._end)
	
	def InitialState(self):
		self.bot = Bot(self.maze, None, self.DISPLAYSURF, self.SIZE)
		self.CreateMenu()
		self.bot.view = self.menu_discover.btn_show_map
		self.bot.draw()

	def CreateMenu(self):
		self.list_menu = [None, None]
		self.menu_discover = MenuDiscover(self.bot, self.maze, self.DISPLAYSURF, self.SPEED, self.list_menu)
		self.menu_solve = MenuSolve(self.bot, self.maze, self.DISPLAYSURF, self.SPEED, self.list_menu)
		self.list_menu[0] = self.menu_discover
		self.list_menu[1] = self.menu_solve

	def run(self):
		FPS = 60
		fpsClock = pygame.time.Clock()
		while True:
			fpsClock.tick(FPS)
			x, y = pygame.mouse.get_pos()
			self.bot.CountAndRemember()
			self.menu_discover.ShowAndAct(x, y)
			self.menu_solve.ShowAndAct(x, y)
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = self.menu_discover.ClickButtons(x,y)
					x, y = self.menu_solve.ClickButtons(x,y, self)

				if event.type == pygame.KEYDOWN:
					if event.key in [K_s, K_DOWN] and self.bot.CheckStateButtons(self.menu_discover.list_btn_discover):
						self.bot.MoveDown()
					if event.key in [K_w,K_UP] and self.bot.CheckStateButtons(self.menu_discover.list_btn_discover):
						self.bot.MoveUp()
					if event.key in [K_a, K_LEFT] and self.bot.CheckStateButtons(self.menu_discover.list_btn_discover):
						self.bot.MoveLeft()
					if event.key in [K_d, K_RIGHT] and self.bot.CheckStateButtons(self.menu_discover.list_btn_discover):
						self.bot.MoveRight()
			pygame.display.update()
			
if __name__ == "__main__":
	game = Game()
	game.run()			


