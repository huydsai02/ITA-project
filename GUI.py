import pygame, sys
from pygame.locals import *
from CreateMatrix import Maze
from Bot import Bot
from SimpleButtons import ButtonShowMap, ButtonNewGame, ButtonAgain
from ButtonShowSolution import ButtonShowSolution
from ButtonSolve import ButtonSolve
from ButtonBestPath import ButtonBestPath
from Color import *

class Game(object):
	SPEED = 1
	_size = (41,41); _num_point = 60; _start = (1,1); _end = (39,39)
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
		self.CreateButton()
		self.bot = Bot(self.maze, self.btn_show_map, self.DISPLAYSURF, self.SIZE)
		self.bot.draw()

	def CreateButton(self):
		self.btn_again = ButtonAgain(pos = (775,150), screen = self.DISPLAYSURF)
		self.btn_new_game = ButtonNewGame(pos = (775,200), screen = self.DISPLAYSURF)
		self.btn_show_map = ButtonShowMap(pos = (775,250), screen = self.DISPLAYSURF)
		self.btn_show_solution = ButtonShowSolution(pos = (775,300), screen = self.DISPLAYSURF)
		self.btn_best_path = ButtonBestPath(pos = (775,350), screen = self.DISPLAYSURF, SPEED = self.SPEED)
		self.btn_dfs = ButtonSolve(alg = "dfs", pos = (775,400), screen = self.DISPLAYSURF, maze = self.maze, solution=self.btn_show_solution,best_path=self.btn_best_path, SPEED = self.SPEED)
		self.btn_a = ButtonSolve(alg = "a*", pos = (775,450), screen = self.DISPLAYSURF, maze = self.maze, SPEED = self.SPEED)
		self.btn_bfs = ButtonSolve(alg = "bfs", pos = (775,500), screen = self.DISPLAYSURF, maze = self.maze, SPEED = self.SPEED)
		self.list_buttons = [self.btn_show_solution, self.btn_bfs, self.btn_dfs, self.btn_a, self.btn_best_path]

	def ShowAndActButtons(self,x,y):
		self.btn_new_game.ShowAndAct(x,y)
		self.btn_again.ShowAndAct(x,y)
		self.btn_show_map.ShowAndAct(x,y)
		self.btn_show_solution.ShowAndAct(x,y)
		self.btn_dfs.ShowAndAct(x,y, self.bot)
		self.btn_a.ShowAndAct(x,y,self.bot)
		self.btn_bfs.ShowAndAct(x,y,self.bot)
		self.btn_best_path.ShowAndAct(x,y,self.bot)
	
	def GradeTable(self):
		pygame.draw.rect(self.DISPLAYSURF, BACKGROUND_COLOR, (775,10,300,115))
		self.DISPLAYSURF.blit(self.ShowInfo(f'TOTAL POINT: {self.bot.point}', size=20), (785, 25))
		self.DISPLAYSURF.blit(self.ShowInfo(f'TOTAL STEP: {self.bot.step}', size=20), (785, 55))
		stri = f'FINAL POINT: {round(self.bot.point/self.bot.step,2)}' if self.bot.step != 0 else 'FINAL POINT: 0'
		self.DISPLAYSURF.blit(self.ShowInfo(stri, size=20), (785, 85))

	def ClickButtons(self,x, y):
		self.btn_show_map.click(x,y, self.bot)
		self.btn_new_game.click(x,y,self)
		self.btn_again.click(x,y,self)
		self.btn_show_solution.click(x,y, self.btn_show_map, self.bot)
		self.btn_best_path.click(x,y, bot = self.bot, solution = self.btn_show_solution, show_map= self.btn_show_map, l = self.list_buttons)
		self.btn_dfs.click(x,y, bot = self.bot, solution = self.btn_show_solution, show_map= self.btn_show_map, l = self.list_buttons, best_path=self.btn_best_path)
		self.btn_a.click(x,y, bot = self.bot, solution = self.btn_show_solution, show_map= self.btn_show_map, l = self.list_buttons, best_path=self.btn_best_path)
		self.btn_bfs.click(x,y, bot = self.bot, solution = self.btn_show_solution, show_map= self.btn_show_map, l = self.list_buttons, best_path=self.btn_best_path)
	
	def ShowInfo(self,Info, size=30):
		fnt = pygame.font.Font('freesansbold.ttf', size)
		text = fnt.render(str(Info), True, COLOR_SHOW_INFO)
		return text
	def run(self):
		FPS = 60
		fpsClock = pygame.time.Clock()
		while True:
			fpsClock.tick(FPS)
			x, y = pygame.mouse.get_pos()
			self.bot.CountAndRemember()
			self.ShowAndActButtons(x,y)		
			self.GradeTable()
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.ClickButtons(x,y)
				if event.type == pygame.KEYDOWN:
					if event.key in [K_s, K_DOWN] and self.bot.CheckStateButtons(self.list_buttons):
						self.bot.MoveDown()
					if event.key in [K_w,K_UP] and self.bot.CheckStateButtons(self.list_buttons):
						self.bot.MoveUp()
					if event.key in [K_a, K_LEFT] and self.bot.CheckStateButtons(self.list_buttons):
						self.bot.MoveLeft()
					if event.key in [K_d, K_RIGHT] and self.bot.CheckStateButtons(self.list_buttons):
						self.bot.MoveRight()
			pygame.display.update()
if __name__ == "__main__":
	game = Game()
	game.run()			


