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

def AllNeedInfo(size = (21,21), num_point = 10, start = None, end = None, multi_path = False):
  width, height = size
  if start == None and end == None:
    while True:
      s = (random.choice(range(1,width - 2,2)),random.choice(range(1,height - 2,2)))
      e = (random.choice(range(1,width - 2,2)),random.choice(range(1,height - 2,2)))
      if ((s[0]-e[0])**2) + ((s[1]-e[1])**2) >= (min(size)-3):
        break
  else:
    s = start
    e = end
  maze = Maze(size = (width, height), num_point= num_point, start = s, end = e, multi_path = False)
  cp = TakeCoordinatePoint(maze)
  cr, cb = TakeCoordinateRoad(maze)
  (score, optimal_path, len_of_best, op_road), path_bot_go, main_path = Optimize_solution(maze)
  highest_score = score / len_of_best
  point_of_best = score
  return maze, cp, cr, cb, score, optimal_path, len_of_best, highest_score, point_of_best, path_bot_go, main_path, op_road

if __name__ == '__main__':
  maze, cp1, cr, cb, score, optimal_path, len_of_best, highest_score, point_of_best, path_bot_go, main_path, op_road = AllNeedInfo(size = (11,11), num_point = 7, start = (1,1), end = (5,5), multi_path = False)
