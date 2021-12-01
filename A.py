from CreateMatrix import *

def FindValidDimension(coordinate, list_maze, p = None):
  # Return dimension which is not wall. If p != None, the opposite dimension of p will take the first position
  steps = [(0,1), (0,-1), (1,0), (-1,0)]
  res = [] if p == None else [((-1) * p[0], (-1) * p[1])]
  for step in steps:
    if list_maze[coordinate[0] + step[0]][coordinate[1] + step[1]] != 1 and step not in res:
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
  return res, same_extra

def TakeExtraPath(dict_path, main_path):
  list_consider = list(dict_path.keys())
  dict_extra_path = {}
  for point in list_consider:
    path = dict_path[point]
    extra_path = []
    for p in path:
      if p not in main_path:
        extra_path.append(p)
    if len(extra_path) > 0:
      dict_extra_path[point] = extra_path
  return dict_extra_path

def BestGainAlley(maze, dict_extra_path):
  list_point = maze.get_list_point()
  full_info, info_all_alleys = Find_Subset(dict_extra_path)
  max_in_alley = 0
  best_alley = ([], 0, 0, 0, [])
  for inp in info_all_alleys:
    consider_list = FullSituation(inp)[1:]
    for subset in consider_list:
      all_cell = []
      cell_have_point = []
      for coordinate in list(subset):      
        all_cell += dict_extra_path[coordinate]
        cell_have_point += full_info[coordinate][1]
      score = sum([list_point[x][y] for x, y in list(set(cell_have_point))])
      step = 2*len(set(all_cell))
      formula = score / step
      if formula > max_in_alley:
        best_alley = (subset, formula, score, step, all_cell)
        max_in_alley = formula
  return best_alley

def ExpandNode(maze, dict_path, current_best_road, sum_point, step, highest_result):
  dict_alley = TakeExtraPath(dict_path, current_best_road)
  info = BestGainAlley(maze, dict_alley)
  if info[1] > highest_result:
    sum_point += info[2]
    step += info[3]
    highest_result = sum_point/step
    current_best_road = list(set(current_best_road + info[4]))
  return (current_best_road, sum_point, step, highest_result)

def Optimal_solution(maze, alg):
  size = maze.get_size()
  end_point = maze.get_end_point()
  list_point = maze.get_list_point()
  list_consider = [(i, j) for i in range(size[0]) for j in range(size[1]) if list_point[i][j] != 0 or (i,j) == end_point]
  dict_path, path_bot_go = FindPath(maze, list_consider, alg)
  main_path = dict_path[end_point]
  current_best_road = main_path[:]
  sum_point = sum([list_point[x][y] for x, y in main_path])
  step = len(main_path) - 1
  highest_result = sum_point / step
  while True:
    old_len = len(current_best_road)
    current_best_road, sum_point, step, highest_result = ExpandNode(maze, dict_path, current_best_road, sum_point, step, highest_result)
    if len(current_best_road) == old_len:
      break
  full_step = PathAllPoint(maze, main_path, current_best_road)
  return sum_point, current_best_road, step, full_step, path_bot_go, main_path

def DimRightRoad(coordinate, main_path, total_path, p = None):
  # Return the dimension which can come to one cell special
  steps = [(0,1), (0,-1), (1,0), (-1,0)]
  res = [] if p == None else [((-1) * p[0], (-1) * p[1])]
  for step in steps:
    if step not in res and (coordinate[0] + step[0],coordinate[1] + step[1]) in main_path:
      res.append(step)
  for step in steps:
    if step not in res and (coordinate[0] + step[0],coordinate[1] + step[1]) in total_path:
      res.append(step) 
  return res

def PathAllPoint(maze, main_path, total_path):
  xs, ys = maze.get_start_point()
  points = total_path[:]
  coors = [(xs, ys)]
  d = {}
  d[(xs, ys)] = DimRightRoad((xs,ys), main_path, total_path)
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
      d[(xs,ys)] = d.get((xs,ys), DimRightRoad((xs,ys), main_path, total_path, p = cpath))
      if (xs, ys) not in coors:
        coors.append((xs, ys))

def del_relate_info(l1, d):
  return list(set(l1) - set(d[0] + d[1]))

def FullSituation(inp):
  s = list(inp.keys())
  d = {}
  for point in s:
    a = (point,)
    d[a] = del_relate_info(s, inp[point])
  res = [[]]
  for ss in ChoosePoint(inp, d):
    res.append(list(ss))
  return res

def ChoosePoint(inp, res, n = 1):
  l = [i for i in list(res.keys())[:] if len(i) == n]
  if len(l) == 0:
    return list(res.keys())
  a = []
  for i in l:
    for j in res[i]:
      ni = list(i)
      ni.append(j)
      if set(ni) not in a:
        a.append(set(ni))
        nl = del_relate_info(res[i], inp[j])
        res[tuple(ni)] = nl
  return ChoosePoint(inp, res, n+1)
