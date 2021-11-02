import pygame
from Color import *
class Bot(object):

	def __init__(self, maze, view, screen, size_screen):
		self.maze = maze
		self.InitialBot()		
		self.view = view
		self.screen = screen
		self.size_screen = size_screen			
	def InitialBot(self):
		maze = self.maze
		self.oc = self.nc = maze.get_start_point()
		self.PathHasGone = [self.nc]
		self.list_point = [maze.get_list_point()[i][:] for i in range(len(maze.get_list_point()))]
		self.decrease = 0
		self.step = 0
		self.point = 0
		self.lr, self.lb = self.maze.TakeCoordinateRoad()		
		self.lp = self.maze.TakeCoordinatePoint()
	def draw(self):
		lr, lb, lp = self.lr, self.lb, self.lp
		size = self.maze.get_size()
		self.side = int(min(self.size_screen)/max(size))
		if self.view.get_state() == False:
			self.DrawRectangle(lr+lb, BACKGROUND_COLOR)
			self.decrease = 1
			self.DrawRectangle(lr+lb, SEED_COLOR)
			self.DrawRectangle(self.PathHasGone, COLOR_ROAD)
			for i, j in self.Around():
				if self.maze.get_list_maze()[i][j] == 1:
					self.DrawRectangle([(i,j)], COLOR_BRICK)
				else:
					self.DrawRectangle([(i,j)], COLOR_ROAD)
			self.DrawRectangle(lp, COLOR_END)

		elif self.view.get_state() == True:
			self.decrease = 0
			self.DrawRectangle(lr, COLOR_ROAD)
			self.DrawRectangle(lb, COLOR_BRICK)
		self.DrawCircle([self.maze.get_end_point()], COLOR_END)
		self.write_score()
		self.DrawCircle([self.nc], COLOR_START)
	
	def DrawRectangle(self, l, color):
		decrease = self.decrease
		side = self.side
		for (i, j) in l:
			pygame.draw.rect(self.screen, color, (i * side + decrease, j * side + decrease, side - 2 * decrease, side - 2 * decrease))

	def DrawCircle(self,l, color):
		decrease = self.decrease
		radius = self.side // 2
		side = self.side
		for (x, y) in l:
			pygame.draw.circle(self.screen, color, (x*side + side/2, y*side + side/2), radius-2*decrease)

	def write_score(self):
		side = self.side
		font = pygame.font.Font('freesansbold.ttf', side // 2)
		decrease = self.decrease
		l = self.maze.TakeCoordinatePoint()
		lp = self.list_point
		for i, j in l:
			text = font.render(str(lp[i][j]), True, COLOR_SCORE)
			text_size = text.get_size()
			x = (side - text_size[0]) // 2
			y = (side - text_size[1]) // 2
			self.screen.blit(text, (x + i * side + decrease, y + j * side + decrease))

	def Around(self):
		dim = [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1), (0,0)]
		x, y = self.nc
		res = [(x+i,y+j) for i, j in dim]
		return res

	def CountAndRemember(self):
		if self.nc != self.oc:
			self.step += 1
			self.oc = self.nc
			self.point += self.list_point[self.nc[0]][self.nc[1]]
			self.list_point[self.nc[0]][self.nc[1]] = 0
			self.draw()
		if self.nc not in self.PathHasGone:
			self.PathHasGone.append(self.nc)
		
	def MoveDown(self):
		xs, ys = self.nc
		cr = self.maze.TakeCoordinateRoad()[0]
		if (xs,ys+1) in cr:
			ys += 1
		self.nc = (xs, ys)

	def MoveUp(self):
		xs, ys = self.nc
		cr = self.maze.TakeCoordinateRoad()[0]
		if (xs,ys-1) in cr:
			ys -= 1
		self.nc = (xs, ys)

	def MoveLeft(self):
		xs, ys = self.nc
		cr = self.maze.TakeCoordinateRoad()[0]
		if (xs-1,ys) in cr:
			xs -= 1
		self.nc = (xs, ys)		

	def MoveRight(self):
		xs, ys = self.nc
		cr = self.maze.TakeCoordinateRoad()[0]
		if (xs+1,ys) in cr:
			xs += 1
		self.nc = (xs, ys)
		
        

        
