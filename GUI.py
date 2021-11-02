import pygame, sys
from pygame.locals import *
from CreateMatrix import Maze
from Bot import Bot
from ButtonShowMap import ButtonShowMap
from ButtonShowSolution import ButtonShowSolution
from NewMazeAndAgain import ButtonNewGame, ButtonAgain
from ButtonSolve import ButtonSolve
from ButtonBestPath import ButtonBestPath

class Game(object):
	SPEED = 1
	_size = (41,41); _num_point = 20; _start = (1,1); _end = (39,39)
	BACKGROUND_COLOR = (55, 155, 255)
	SIZE = (1050,670)
	COLOR_TEST = (0,0,0)

	def __init__(self):
		pygame.init()
		self.DISPLAYSURF = pygame.display.set_mode((self.SIZE[0], self.SIZE[1]))
		pygame.display.set_caption('Maze')
		self.DISPLAYSURF.fill(self.BACKGROUND_COLOR)
		self.NewMaze()
		self.InitialState()		
	
	def NewMaze(self):
		self.maze = Maze(size = self._size, num_point = self._num_point, start = self._start, end = self._end)
		self.InitialState()
	
	def InitialState(self):
		self.CreateButton()
		self.bot = Bot(self.maze, self.btn_show_map, self.DISPLAYSURF, self.SIZE)
		self.bot.draw()

	def CreateButton(self):
		self.btn_again = ButtonAgain(pos = (775,100), screen = self.DISPLAYSURF)
		self.btn_new_game = ButtonNewGame(pos = (775,150), screen = self.DISPLAYSURF)
		self.btn_show_map = ButtonShowMap(pos = (775,200), screen = self.DISPLAYSURF)
		self.btn_show_solution = ButtonShowSolution(pos = (775,250), screen = self.DISPLAYSURF)
		self.btn_best_path = ButtonBestPath(pos = (775,300), screen = self.DISPLAYSURF, SPEED = self.SPEED)
		self.btn_dfs = ButtonSolve(alg = "dfs", pos = (775,350), screen = self.DISPLAYSURF, maze = self.maze, solution=self.btn_show_solution,best_path=self.btn_best_path, SPEED = self.SPEED)
		self.btn_a = ButtonSolve(alg = "a*", pos = (775,400), screen = self.DISPLAYSURF, maze = self.maze, SPEED = self.SPEED)
		self.btn_bfs = ButtonSolve(alg = "bfs", pos = (775,450), screen = self.DISPLAYSURF, maze = self.maze, SPEED = self.SPEED)
		self.list_buttons = [self.btn_show_solution, self.btn_bfs, self.btn_dfs, self.btn_a, self.btn_best_path]

	def ShowButtons(self,x,y):
		self.btn_new_game.show(x,y)
		self.btn_again.show(x,y)
		self.btn_show_map.show(x,y)
		self.btn_show_solution.show(x,y)
		self.btn_dfs.show(x,y)
		self.btn_a.show(x,y)
		self.btn_bfs.show(x,y)
		self.btn_best_path.show(x,y)

	def ActiveButtons(self):
		self.btn_show_map.active()
		self.btn_show_solution.active()
		self.btn_dfs.active(self.bot)
		self.btn_a.active(self.bot)
		self.btn_bfs.active(self.bot)
		self.btn_best_path.active(self.bot)
	def ClickButtons(self,x, y):
		self.btn_show_map.click(x,y, self.bot)
		self.btn_new_game.click(x,y,self)
		self.btn_again.click(x,y,self)
		self.btn_show_solution.click(x,y, self.btn_show_map, self.bot)
		self.btn_best_path.click(x,y, bot = self.bot, solution = self.btn_show_solution, show_map= self.btn_show_map, l = self.list_buttons)
		self.btn_dfs.click(x,y, bot = self.bot, solution = self.btn_show_solution, show_map= self.btn_show_map, l = self.list_buttons, best_path=self.btn_best_path)
		self.btn_a.click(x,y, bot = self.bot, solution = self.btn_show_solution, show_map= self.btn_show_map, l = self.list_buttons, best_path=self.btn_best_path)
		self.btn_bfs.click(x,y, bot = self.bot, solution = self.btn_show_solution, show_map= self.btn_show_map, l = self.list_buttons, best_path=self.btn_best_path)
	
	def run(self):
		FPS = 60
		fpsClock = pygame.time.Clock()
		while True:
			fpsClock.tick(FPS)
			x, y = pygame.mouse.get_pos()
			self.bot.CountAndRemember()
			self.ShowButtons(x,y)
			self.ActiveButtons()			
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.ClickButtons(x,y)
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


