from CreateMatrix import *
import numpy as np
import itertools
import random

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

def FindPath(maze,start = (1,1) ,end = None, c = None, points = None, dict = {}): #Lỗi logic hàm này
  xs, ys = start
  list_maze = maze.get_list_maze()
  d = {}
  coors = [(xs, ys)]
  d[(xs, ys)] = FindValidDimension((xs,ys), list_maze, c)
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
      if (xs, ys) not in coors:
        coors.append((xs, ys))
    # print(coors[-1], (xs,ys))
    if (xs, ys) in dict and False:
      path = dict[(xs, ys)]
      same = []
      diff = []
      for a1 in coors:
        if a1 not in path:
          diff.append(a1)
        else:
          same.append(a1)
      
      c_diff = diff[:]
      for x, y in same:
        if (x-1, y) in c_diff or (x+1, y) in c_diff or (x, y-1) in c_diff or (x, y+1) in c_diff:
          diff.append((x,y))
      
      for b1 in path:
        if b1 not in same:
          diff.append(b1)

      return diff
      
    if end == None and points != None:
      if (xs, ys) in points:
        return coors
    else:
      if (xs, ys) == end:
        return coors


def ConsiderCell(maze, path = []):
  size = maze.get_size()
  list_point = maze.get_list_point()
  res = []
  for x in range(size[0]):
    for y in range(size[1]):
      if list_point[x][y] != 0 and (x,y) not in path:
        res.append((x, y))
  return res

def Optimize_solution(maze):
  start = maze.get_start_point()
  end = maze.get_end_point()
  list_point = maze.get_list_point()
  size = maze.get_size()
  main_path = FindPath(maze = maze, start = start, end = end)
  consider_cell = ConsiderCell(maze, path = main_path)
  max = 0
  diction_road = {}
    
  # all_path = []
  for sl in range(0, len(consider_cell) + 1):
    for subset in itertools.combinations(consider_cell, sl):
      l = [[0 for i in range(size[1])] for j in range(size[0])]
      for i in range(size[0]):
        for j in range(size[1]):
          if (i, j) not in main_path:
            l[i][j] = Cell((i,j), maze, main_road = False)
          else:
            l[i][j] = Cell((i,j), maze, main_road = True)
      total_path = main_path[:]
      lss = list(subset)
      for coordinate in lss:
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
      # all_path.append((score, length))
      formular = score / length
      if formular >= max:
        op = (score, total_path, length)
        max = formular
  return op

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


  # list_maze = maze.get_list_maze()
  # list_point = maze.get_list_point()
  # print(np.array(list_maze))
  # print(np.array(list_point))


  

 
