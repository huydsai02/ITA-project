from CreateMatrix import *
import numpy as np
import itertools
import random

########### Ý tưởng sẽ là mình đi từ điểm xuất phát đến điểm cuối cùng, trên đường mình gặp cái điểm nào thì mình sẽ ghi lại điểm đó.
########### Khi mình đến điểm cuối cùng thì sẽ còn những nơi có điểm mình chưa tới. Khi đó, từ điểm cuối cùng, mình sẽ đi tìm tất cả 
########### những nơi có điểm còn lại

class Cell(object):
  def __init__(self, coor, maze, main_road = False):
    self.x = coor[0]
    self.y = coor[1]
    self.maze = maze    
    self.main_road = main_road
    if main_road == False:
      self.times = 0
      self.go_through = False
    else:      
      self.times = 1
      self.go_through = True

  def TimesGoPoint(self):
    maze = self.maze
    x, y = self.get_pos()
    if maze.get_list_maze()[x][y] != 1:
      valid_dimension = len(FindValidDimension((x,y) , maze.get_list_maze()))
      times = self.times
      if times < valid_dimension:
        times += 1
      self.times = times
    return self.times
  
  def IsEnd(self, l):
    x, y = self.get_pos()
    count = 0
    if l[x][y-1].go_through == True:
      count += 1
    if l[x][y+1].go_through == True:
      count += 1
    if l[x-1][y].go_through == True:
      count += 1
    if l[x+1][y].go_through == True:
      count += 1
    if count == 1 or (x,y) == self.maze.get_start_point():
      return True
    else:
      return False

  def GoThrough(self):
    self.go_through = True 

  def get_pos(self):
    return (self.x, self.y)

  def get_times(self):
    return self.times

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

def FindPath(maze, points = []):
  xs, ys = maze.get_start_point()
  list_maze = maze.get_list_maze()
  coors = [(xs, ys)]
  dict_road = {}
  d = {}
  d[(xs, ys)] = FindValidDimension((xs,ys), list_maze)
  path_bot_go = [[(xs,ys), d[(xs,ys)][:]]]
  while True:
    if len(d[coors[-1]]) == 0:
      coors.pop()
      xs, ys = coors[-1]
    else:
      dim = d[(xs,ys)]
      cpath = dim.pop()
      xs += cpath[0]
      ys += cpath[1]
      d[(xs,ys)] = d.get((xs,ys), FindValidDimension((xs,ys), list_maze, p = cpath))
      path_bot_go.append([(xs,ys), d[(xs,ys)][:]])
      if (xs, ys) not in coors:
        coors.append((xs, ys))

    if (xs, ys) in points:
      road = coors[:]
      dict_road[(xs, ys)] = road
      new_points = [point for point in points if point != (xs, ys)]
      points = new_points
    if len(points) == 0:
      return dict_road, path_bot_go
    
def MazeAnalysis(maze):
  size = maze.get_size()
  start_point = maze.get_start_point()
  end_point = maze.get_end_point()
  list_point = maze.get_list_point()
  list_consider = [(i, j) for i in range(size[0]) for j in range(size[1]) if list_point[i][j] != 0 or (i,j) == end_point]
  dict_path, path_bot_go = FindPath(maze, list_consider)
  main_path = dict_path[end_point]
  dict_extra_path = {}
  for point in list_consider:
    if point != end_point:
      path = dict_path[point]
      extra_path = []
      for p in path:
        if p not in main_path:
          extra_path.append(p)
      if len(extra_path) > 0:
        dict_extra_path[point] = extra_path
  return main_path, dict_extra_path, path_bot_go
  
def Optimize_solution(maze):
  list_point = maze.get_list_point()
  size = maze.get_size()
  main_path, diction_road, path_bot_go = MazeAnalysis(maze)
  max = 0
  start_extra = Find_Subset(diction_road)
  list_subset = MixPoint(start_extra)

  for subset in list_subset:

    l = [[0 for i in range(size[1])] for j in range(size[0])]
    for i in range(size[0]):
      for j in range(size[1]):
        if (i, j) not in main_path:
          l[i][j] = Cell((i,j), maze, main_road = False)
        else:
          l[i][j] = Cell((i,j), maze, main_road = True)

    total_path = main_path[:]

    for coordinate in list(subset):
      if coordinate not in diction_road:
        extra_path = FindPath(maze = maze, start = coordinate, points = main_path, dict = diction_road)
        diction_road[coordinate] = extra_path
      else:
        extra_path = diction_road[coordinate]
      for coo in extra_path:
        l[coo[0]][coo[1]].TimesGoPoint()
        if coo not in total_path:
          total_path.append(coo)
          l[coo[0]][coo[1]].TimesGoPoint()

    score = 0
    length = 1
    for concoor in total_path:
      score += list_point[concoor[0]][concoor[1]]
      cell = l[concoor[0]][concoor[1]]
      if cell.IsEnd(l):
        length += (cell.get_times() - 1)
      else:
        length += cell.get_times()

    formular = score / length
    if formular >= max:
      op = (score, total_path, length)
      max = formular

  return op, path_bot_go, main_path

def Find_Subset(d):
  # Hàm trả về những đầu mút của đường thêm
  l = list(d.keys())
  res = {}
  for consider in l:
    # tập b là tập những điểm không nằm trong danh sách consider đi qua (trừ nó)
    b = [consider]
    # tập c là tập những điểm phải đi qua mới đến consider được
    c = [consider]
    for _ in l:
      if consider in d[_]:
          b.append(_)
      if _ in d[consider]:
          c.append(_)
    b = list(set(b))
    c = list(set(c))
    if len(c) == 1:
      res[consider] = b
  return res

def MixPoint(d):
  l = list(d.keys())
  list_d = []
  res = [list_d]
  for L in range(1,len(l) + 1):
    for subset in itertools.combinations(l, L):
      list_d = []
      for choosen in list(subset):
        list_d.append(d[choosen])
      a = CombineList(list_d)
      for i in a:
        res.append(i)
  return res
            
def CombineList(l):
  lf = []
  ln = len(l)
  if ln == 1:
    return [[i] for i in l[0]]
  for i in l[-1]:
    for j in CombineList(l[:ln-1]):
      j.append(i)
      lf.append(j)
  return lf


if __name__ == '__main__':
  while True:
    si = 15
    s = (random.choice(range(1,si - 2,2)),random.choice(range(1,si-2,2)))
    e = (random.choice(range(1,si - 2,2)),random.choice(range(1,si - 2,2)))
    maze = Maze(size = (si,si), start = s, end = e, num_point = 5)
    coordinate = (random.choice(range(1,si - 2,2)),random.choice(range(1,si - 2,2)))
    main_path = FindPath(maze = maze, end = e, start=s)
    extra_path = FindPath(maze = maze, start = coordinate, points = main_path)
    print(Optimize_solution(maze))

def FindDimensionIsPath(coor, main_path, total_path, p = None):
  # Hàm trả về các hướng không phải tường 
  # điểm cuối sẽ là hướng p nếu hướng p ko có gạch, điểm đầu sẽ là hướng ngược lại p
  steps = [(0,1), (0,-1), (1,0), (-1,0)]
  # phan_bu = [c for c in total_path if c not in main_path]
  if p != None:
    a = (-1) * p[0]
    b = (-1) * p[1]
    res = [(a,b)]
    for step in steps:
      if step not in res and (coor[0] + step[0],coor[1] + step[1]) in main_path:
        res.append(step)
      elif step not in res and (coor[0] + step[0],coor[1] + step[1]) in total_path:
        res.append(step)

  else:
    res = []
    for step in steps:
      if step not in res and (coor[0] + step[0],coor[1] + step[1]) in main_path:
        res.append(step)
      elif step not in res and (coor[0] + step[0],coor[1] + step[1]) in total_path:
        res.append(step) 
  return res

def FindOptimalPath(maze, main_path, total_path):
  xs, ys = maze.get_start_point()
  points = total_path[:]
  coors = [(xs, ys)]
  d = {}
  d[(xs, ys)] = FindDimensionIsPath((xs,ys), main_path, total_path)
  path_bot_go = [[(xs,ys), d[(xs,ys)][:]]]
  while True:
    if len(d[coors[-1]]) == 0:
      coors.pop()
      xs, ys = coors[-1]
    else:
      dim = d[(xs,ys)]
      cpath = dim.pop()
      xs += cpath[0]
      ys += cpath[1]
      d[(xs,ys)] = d.get((xs,ys), FindDimensionIsPath((xs,ys), main_path, total_path, p = cpath))
      path_bot_go.append([(xs,ys), d[(xs,ys)][:]])
      if (xs, ys) not in coors:
        coors.append((xs, ys))

    if (xs, ys) in points:
      new_points = [point for point in points if point != (xs, ys)]
      points = new_points
    if len(points) == 0 and (xs, ys) == maze.get_end_point():
      return path_bot_go