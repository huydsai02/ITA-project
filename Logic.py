from CreateMatrix import *
import numpy as np
import itertools
import random

class Cell(object):
  def __init__(self, coor, maze, main_road = False):
    self.x = coor[0]
    self.y = coor[1]
    self.maze = maze
    self.info_road = self.RoadGoThrough()
    self.main_road = main_road
    self.choice = len(self.info_road)
    
  
  def get_pos(self):
    return (self.x, self.y)

  def get_info_road(self):
    return self.info_road

  def RoadGoThrough(self):
    maze = self.maze
    self.info_road = {}
    self.valid_dimension = FindValidDimension(self.get_pos() , maze.get_list_maze())
    for d in self.valid_dimension:
      road = FindPath(self.maze, start = self.get_pos(), c = d)
      self.info_road[d] = Road(road, maze)
    return self.info_road

class Road(object):
  def __init__(self, route, maze):
    self.route = route
    self.maze = maze
    self.AnalysisRoad()

  def AnalysisRoad(self):
    route = self.route
    list_point = self.maze.get_list_point()
    self.start = route[0]
    self.end = route[-1]
    self.point = list_point[self.start[0]][self.start[1]]
    self.length = len(route) - 1

  def get_start(self):
    return self.start

  def get_end(self):
    return self.end

  def get_route(self):
    return self.route
  
  def get_point(self):
    return self.point
  
  def get_length(self):
    return self.length




# Hàm bên ngoài phụ trợ
def FindValidDimension(coor, list_maze, p = None):
  # Hàm trả về các hướng không phải tường 
  # điểm cuối sẽ là hướng p nếu hướng p ko có gạch, điểm đầu sẽ là hướng ngược lại p
  steps = [(0,1), (0,-1), (1,0), (-1,0)]
  if p != None:
    a = (-1) * p[0]
    b = (-1) * p[1]
    res = [(a,b)]
    for step in steps:
      if step not in res and list_maze[coor[0] + step[0]][coor[1] + step[1]] != 1 and step != p:
        res.append(step)
    if list_maze[coor[0] + p[0]][coor[1] + p[1]] != 1:
      res.append(p)
  else:
    res = []
    for step in steps:
      if list_maze[coor[0] + step[0]][coor[1] + step[1]] != 1:
        res.append(step)
  
  return res

def FindPath(maze,start = (1,1) ,end = None, c = None, path = None):
  xs, ys = start
  list_maze = maze.get_list_maze()
  d = {}
  coors = [(xs, ys)]
  d[(xs, ys)] = FindValidDimension((xs,ys), list_maze, c)
  while True:
    if len(d[coors[-1]]) == 0:
      coors.pop()
      xs, ys = coors.pop()
    else:
      dim = d[(xs,ys)]
      cpath = dim.pop()
      xs += cpath[0]
      ys += cpath[1]
      d[(xs,ys)] = d.get((xs,ys), FindValidDimension((xs,ys), list_maze, p = cpath))
      if (xs, ys) not in coors:
        coors.append((xs, ys))
    if end == None and path == None:
      if (xs, ys) in StopCell(maze):
        return coors
    elif end == None:
      if (xs, ys) in path:
        return coors
    else:
      if (xs, ys) == end:
        return coors


def StopCell(maze):
  size = maze.get_size()
  list_maze = maze.get_list_maze()
  list_point = maze.get_list_point()
  res = []
  for x in range(size[0]):
    for y in range(size[1]):
      if list_maze[x][y] != 1:
        n = len(FindValidDimension((x,y), list_maze))
        a = n == 3 or n == 4 or n == 1
        b = list_point[x][y] != 0 
        c = list_maze[x][y] == 2 or list_maze[x][y] == 3
        if a or b or c:
          res.append((x,y))
  return res

def Optimize_solution(start, end, maze):
  xs, ys = start
  xf, yf = end
  list_maze = maze.get_list_maze()
  list_stop_cell = StopCell(maze)
  list_point = maze.get_list_point()
  size = maze.get_size()
  main_path = FindPath(maze = maze, start = start, end = end)
  l = [[0 for i in range(size[1])] for j in range(size[0])]
  not_main_path = []
  for i in range(size[0]):
    for j in range(size[1]):
      if (i,j) in list_stop_cell:
        if (i,j) in main_path:
          l[i][j] = Cell((i,j), maze, main_road = True)
        else:
          not_main_path.append((i,j))
          l[i][j] = Cell((i,j), maze, main_road = False)
  all_path = []
  for sl in range(0, len(not_main_path) + 1):
    for subset in itertools.combinations(not_main_path, sl):
      total_path = main_path[:]
      lss = list(subset)
      for coordinate in lss:
        extra_path = FindPath(maze = maze, start = coordinate, path = main_path)
        for eer in extra_path:
          if eer not in main_path:
            total_path.append(eer)
      score = 0
      for eer1 in total_path:
        if list_point[eer1[0]][eer1[1]] != 0:
          score += list_point[eer1[0]][eer1[1]]
      all_path.append((score, len(total_path)))

if __name__ == '__main__':
  while True:
    s = (random.choice(range(1,19,2)),random.choice(range(1,19,2)))
    e = (random.choice(range(1,19,2)),random.choice(range(1,19,2)))
    maze = Maze(size = (21,21), s= s , e = e)
    coordinate = (random.choice(range(1,19,2)),random.choice(range(1,19,2)))
    main_path = FindPath(maze = maze, end = e, start=s)
    extra_path = FindPath(maze = maze, start = coordinate, path = main_path)
    print(coordinate)
    print(extra_path)

  # print(Optimize_solution(s, e, maze))

  # list_maze = maze.get_list_maze()
  # list_point = maze.get_list_point()
  # print(np.array(list_maze))
  # print(np.array(list_point))


  

 
