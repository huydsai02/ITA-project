from CreateMatrix import *
from Logic import *

def TakeCoordinatePoint(maze):
  lp = maze.get_list_point()
  size = maze.get_size()
  return [(i, j) for i in range(size[0]) for j in range(size[1]) if lp[i][j] != 0]

def TakeCoordinateRoad(maze):
  lm = maze.get_list_maze()
  size = maze.get_size()
  lr = [(i, j) for i in range(size[0]) for j in range(size[1]) if lm[i][j] != 1]
  lb = [(i, j) for i in range(size[0]) for j in range(size[1]) if lm[i][j] == 1]
  return lr, lb

def AllNeedInfo():
  maze = Maze
  width, height = (20, 20)
  s = (random.choice(range(1,width - 2,2)),random.choice(range(1,height - 2,2)))
  e = (random.choice(range(1,width - 2,2)),random.choice(range(1,height - 2,2)))
  maze = Maze(size = (width, height), num_point= 10, start = s, end = e, multi_path = False)
  cp = TakeCoordinatePoint(maze)
  cr, cb = TakeCoordinateRoad(maze)
  (score, optimal_path, len_of_best), main_path, list_start = Optimize_solution(maze)
  highest_score = score / len_of_best
  point_of_best = score
  return maze, cp, cr, cb, score, optimal_path, len_of_best, highest_score, point_of_best