from CreateMatrix import *
import numpy as np
import itertools
import random

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
  main_path, diction_road, path_bot_go = MazeAnalysis(maze)
  max = 0
  full_info = Find_Subset(diction_road)
  print(full_info)
  list_subset = FullSituation(full_info)
  print(list_subset)
  for subset in list_subset:
    total_path = main_path[:]
    for coordinate in list(subset):
      if coordinate not in diction_road:
        extra_path = FindPath(maze = maze, start = coordinate, points = main_path, dict = diction_road)
        diction_road[coordinate] = extra_path
      else:
        extra_path = diction_road[coordinate]
      for coo in extra_path:
        if coo not in total_path:
          total_path.append(coo)
    score = 0
    full_step = FindOptimalPath(maze, main_path, total_path)
    length = len(full_step) - 1
    for concoor in total_path:
      score += list_point[concoor[0]][concoor[1]]
    formular = score / length
    if formular >= max:
      op = (score, total_path, length, full_step)
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
    res[consider] = [b[:],c[:]]
  return res

def FindDimensionIsPath(coor, main_path, total_path, p = None):
  # Hàm trả về các hướng không phải tường 
  # điểm cuối sẽ là hướng p nếu hướng p ko có gạch, điểm đầu sẽ là hướng ngược lại p
  steps = [(0,1), (0,-1), (1,0), (-1,0)]
  if p != None:
    a = (-1) * p[0]
    b = (-1) * p[1]
    res = [(a,b)]
    for step in steps:
      if step not in res and (coor[0] + step[0],coor[1] + step[1]) in main_path:
        res.append(step)
    for step in steps:
      if step not in res and (coor[0] + step[0],coor[1] + step[1]) in total_path:
        res.append(step)
  else:
    res = []
    for step in steps:
      if step not in res and (coor[0] + step[0],coor[1] + step[1]) in main_path:
        res.append(step)
    for step in steps:
      if step not in res and (coor[0] + step[0],coor[1] + step[1]) in total_path:
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
    if (xs, ys) in points:
      new_points = [point for point in points if point != (xs, ys)]
      points = new_points
    if (xs, ys) == maze.get_end_point() and len(points) == 0:
      return path_bot_go
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

def test(first_num, list_copy, d, n):
    ans = []
    list_copy = del_relate_info(list_copy, d[first_num])
    if n == 1:
        return [[i] for i in list_copy]
    if n == 0:
        return []
    for coor1 in list_copy:
        for lc in test(coor1, list_copy, d, n-1):
            lc.append(coor1)
            ans.append(lc)
    return ans

def del_relate_info(l1, d):
    new_l = []
    for point in l1:
        if point not in d[0] and point not in d[1]:
            new_l.append(point)
    return new_l

def FullSituation(d):
  l = list(d.keys())
  lc = l[:]
  cover = [{}]
  for point in l:
    cover.append(set([point]))
  for n in range(1, len(l)+1):
    for start in l:
      for points in test(start, lc, d, n-1):
        points = [start] + points
        if set(points) not in cover:
          cover.append(set(points))
  s = [list(p) for p in cover]    
  return s