from CreateMatrix import *

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

def Manhattan(x1, x2):
  return abs(x1[0] - x2[0]) + abs(x1[1] - x2[1])

def PriorPop(paths, points= []):
  if len(points):
    tpop = float('inf')
    tpath = paths[-1]
    for path in paths:
      m = min([Manhattan(path[-1], point) + len(path) - 1 for point in points])
      if m < tpop:
        tpop = m
        tpath = path
    paths.remove(tpath)
    return tpath
  else:
    return paths.pop(0)

def FindPath(maze, points = [], alg= 'dfs'):
  xs, ys = maze.get_start_point()
  list_maze = maze.get_list_maze()
  coors = [(xs, ys)]
  dict_road = {}
  d = {}
  d[(xs, ys)] = FindValidDimension((xs,ys), list_maze)
  path_bot_go = [[(xs,ys), d[(xs,ys)][:]]]
  if alg == 'dfs':
    while True:
      if len(d[coors[-1]]) == 0:
        coors.pop()
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
      if len(coors) == 0:
        return dict_road, path_bot_go

  elif alg.lower() == 'A*'.lower():
    paths = [[(xs, ys)]]
    while True:
      path = PriorPop(paths, points)
      (xt, yt) = path[-1]
      if len(d[(xt, yt)]):
        for direct in  d[(xt, yt)]:
          x0, y0 = xt + direct[0], yt + direct[1]
          npath = path[:]
          npath.append((x0, y0))
          paths.append(npath)
          direct0 = FindValidDimension((x0, y0), list_maze, p= direct)
          direct0.pop(0)
          d[(x0, y0)] = d.get((x0, y0), direct0)
          path_bot_go.append([(x0, y0), d[(x0, y0)][:]])
          if (x0, y0) in points:
            road = npath
            dict_road[(x0, y0)] = road
            new_points = [point for point in points if point != (x0, y0)]
            points = new_points
      if len(paths) == 0:
        return dict_road, path_bot_go
          
  elif alg == 'bfs':
    paths = [[(xs, ys)]]
    while True:
      path = paths.pop(0)
      (xt, yt) = path[-1]
      if len(d[(xt, yt)]):
        for direct in  d[(xt, yt)]:
          x0, y0 = xt + direct[0], yt + direct[1]
          npath = path[:]
          npath.append((x0, y0))
          paths.append(npath)
          direct0 = FindValidDimension((x0, y0), list_maze, p= direct)
          direct0.pop(0)
          d[(x0, y0)] = d.get((x0, y0), direct0)
          path_bot_go.append([(x0, y0), d[(x0, y0)][:]])
          if (x0, y0) in points:
            road = npath
            dict_road[(x0, y0)] = road
            new_points = [point for point in points if point != (x0, y0)]
            points = new_points
      if len(paths) == 0:
        return dict_road, path_bot_go

    
    
def MazeAnalysis(maze, alg):
  size = maze.get_size()
  end_point = maze.get_end_point()
  list_point = maze.get_list_point()
  list_consider = [(i, j) for i in range(size[0]) for j in range(size[1]) if list_point[i][j] != 0 or (i,j) == end_point]
  dict_path, path_bot_go = FindPath(maze, list_consider, alg)
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
  
def Optimal_solution(maze, alg):
  list_point = maze.get_list_point()
  main_path, dict_extra_path, path_bot_go = MazeAnalysis(maze, alg)
  max = 0
  list_subset = FullSituation(dict_extra_path, list_point)
  sum_point_main = sum(list_point[x][y] for x, y in main_path)
  step_main = len(main_path) - 1
  print(len(list_subset))
  for score, step, points in list_subset:
    total_score = sum_point_main + score
    total_step = step_main + step
    result = total_score/ total_step
    if result > max:
      max = result
      points_add = points
      total_best_score = total_score
      number_best_step = total_step
  best_road = main_path[:]
  for point in points_add:
    best_road += dict_extra_path[point]
  best_road = list(set(best_road))
  full_step = FindOptimalPath(maze, main_path, best_road)
  return total_best_score, best_road, number_best_step, full_step, path_bot_go, main_path

def Find_Subset(d):
  # Hàm trả về những đầu mút của đường thêm
  l = list(d.keys())
  res = {}
  start_extra = {}
  for consider in l:
    # tập b là tập những điểm không nằm trong danh sách consider đi qua (trừ nó)
    b = [consider]
    # tập c là tập những điểm phải đi qua mới đến consider được
    c = [consider]
    start_extra[d[consider][0]] = start_extra.get(d[consider][0],[])
    start_extra[d[consider][0]].append(consider)
    for _ in l:
      if consider in d[_]:
          b.append(_)
      if _ in d[consider]:
          c.append(_)
    b = list(set(b))
    c = list(set(c))
    res[consider] = [b[:],c[:]]
  same_extra = []
  for point in start_extra:
    a1 = {}
    for other_point in start_extra[point]:
      a1[other_point] = res[other_point]
    same_extra.append(a1)
  return same_extra

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
  path_bot_go = []
  while True:
    if (xs, ys) in points:
      new_points = [point for point in points if point != (xs, ys)]
      points = new_points
    if (xs, ys) == maze.get_end_point() and len(points) == 0:
      path_bot_go.append([(xs,ys), [()]])
      return path_bot_go
    if len(d[coors[-1]]) == 0:
      coors.pop()
      xs, ys = coors[-1]
    else:
      dim = d[(xs,ys)]
      cpath = dim.pop()
      path_bot_go.append([(xs,ys), [cpath]])
      xs += cpath[0]
      ys += cpath[1]
      d[(xs,ys)] = d.get((xs,ys), FindDimensionIsPath((xs,ys), main_path, total_path, p = cpath))
      if (xs, ys) not in coors:
        coors.append((xs, ys))

def FullSituation(dict_extra_path, list_point):
  import time
  alleys = Find_Subset(dict_extra_path)
  all = []
  a = False
  for info_alley in alleys:
    t1 = time.time()
    test = OptimizeBackTracking(info_alley, dict_extra_path, list_point)
    t2 = time.time()
    if t2 - t1 > 0.5:
      print("Alley:", len(test))
      print(t2-t1)
      a = True
    all.append(test)
  if a:
    print("DONE")
  return CombineList(all)

def CombineList(l):
  lf = []
  ln = len(l)
  if ln == 1:
    return l[0]
  elif ln == 0:
    return []
  cl = CombineList(l[:ln-1])
  for score1, step1, points1 in l[-1]:
    for score2, step2, points2 in cl:
      lf.append((score1 + score2, step1 + step2, points1 + points2))
  return lf

def Calculate(point_add, old_info, dict_path, dict_prev, list_point):
  old_points = old_info[1]
  score = old_info[2] + sum(list_point[x][y] for x, y in dict_prev[point_add] - old_points)
  new_points = old_points.union(dict_prev[point_add])
  all_cell = old_info[3].union(dict_path[point_add])
  formula = score / (2*len(all_cell))
  return (formula, new_points, score, all_cell)

def OptimizeBackTracking(inp, dict_extra_path, list_point):
  l_key, l_value = [], []
  all = list(inp.keys())
  all_info = [(0,0,[])]
  l_intersect, d_path, d_prev = {}, {}, {}
  for i in range(len(all)):
    d_path[all[i]] = set(dict_extra_path[all[i]])
    d_prev[all[i]] = set(inp[all[i]][1])
    info = Calculate(all[i], (0,set(),0,set()), d_path, d_prev, list_point)
    st = set(all[:i]) - set(inp[all[i]][0]) - set(inp[all[i]][1])
    if len(st) != 0:
      l_key.append(info)
      l_value.append(st)
    l_intersect[all[i]] = st
    all_info.append((info[2], 2*len(info[3]), list(info[1])))
  while True:
    if len(l_key) == 0:
      break
    old_info = l_key.pop()
    points = l_value.pop()
    for point in points:
      new_info = Calculate(point, old_info, d_path, d_prev, list_point)
      new_points = set.intersection(points, l_intersect[point])
      if len(new_points) != 0:
        l_key.append(new_info)
        l_value.append(new_points)
      all_info.append((new_info[2], 2*len(new_info[3]), list(new_info[1])))
  return all_info