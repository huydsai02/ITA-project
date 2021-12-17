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

	# def ShowAndActButtons(self,x,y):
	# 	self.btn_new_game.ShowAndAct(x,y)
	# 	self.btn_again.ShowAndAct(x,y)
	# 	self.btn_show_map.ShowAndAct(x,y)
	# 	self.btn_show_solution.ShowAndAct(x,y)
	# 	self.btn_dfs.ShowAndAct(x,y, self.bot)
	# 	self.btn_a.ShowAndAct(x,y,self.bot)
	# 	self.btn_bfs.ShowAndAct(x,y,self.bot)
	# 	self.btn_best_path.ShowAndAct(x,y,self.bot)
	
	# def GradeTable(self):
	# 	pygame.draw.rect(self.DISPLAYSURF, BACKGROUND_COLOR, (775,10,300,115))
	# 	self.DISPLAYSURF.blit(self.ShowInfo(f'TOTAL POINT: {self.bot.point}', size=20), (785, 25))
	# 	self.DISPLAYSURF.blit(self.ShowInfo(f'TOTAL STEP: {self.bot.step}', size=20), (785, 55))
	# 	stri = f'FINAL POINT: {round(self.bot.point/self.bot.step,2)}' if self.bot.step != 0 else 'FINAL POINT: 0'
	# 	self.DISPLAYSURF.blit(self.ShowInfo(stri, size=20), (785, 85))
	# 	self.DISPLAYSURF.blit(self.ShowInfo('DISCOVER', size = 15), (815, 550))
	# 	pygame.draw.rect(self.DISPLAYSURF, COLOR_SHOW_INFO, (770, 397, 181, 150), 2, 5)

	# def ClickButtons(self,x, y):
	# 	self.btn_show_map.click(x,y, self.bot)
	# 	self.btn_new_game.click(x,y,self)
	# 	self.btn_again.click(x,y,self)
	# 	self.btn_show_solution.click(x,y, self.btn_show_map, self.bot)
	# 	self.btn_best_path.click(x,y, bot = self.bot, solution = self.btn_show_solution, show_map= self.btn_show_map, l = self.list_buttons)
	# 	self.btn_dfs.click(x,y, bot = self.bot, solution = self.btn_show_solution, show_map= self.btn_show_map, l = self.list_buttons, best_path=self.btn_best_path)
	# 	self.btn_a.click(x,y, bot = self.bot, solution = self.btn_show_solution, show_map= self.btn_show_map, l = self.list_buttons, best_path=self.btn_best_path)
	# 	self.btn_bfs.click(x,y, bot = self.bot, solution = self.btn_show_solution, show_map= self.btn_show_map, l = self.list_buttons, best_path=self.btn_best_path)
	
	# def ShowInfo(self,Info, size=20):
	# 	fnt = pygame.font.Font('freesansbold.ttf', size)
	# 	text = fnt.render(str(Info), True, COLOR_SHOW_INFO)
	# 	return text
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
					self.menu_discover.ClickButtons(x,y)
					self.menu_solve.ClickButtons(x,y, self)

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


