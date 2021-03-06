from CreateMatrix import *
import time

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
      if len(points) == 0:
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
      if len(points) == 0:
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
      if len(points) == 0:
        return dict_road, path_bot_go

def Find_Subset(d):
  # H??m tr??? v??? nh???ng ?????u m??t c???a ???????ng th??m
  l = list(d.keys())
  res = {}
  start_extra = {}
  for consider in l:
    # t???p b l?? t???p nh???ng ??i???m kh??ng n???m trong danh s??ch consider ??i qua (tr??? n??)
    b = [consider]
    # t???p c l?? t???p nh???ng ??i???m ph???i ??i qua m???i ?????n consider ???????c
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

def TakeExtraPath(dict_path, main_path):
  list_consider = list(dict_path.keys())
  dict_extra_path = {}
  for point in list_consider:
    extra_path = []
    path = dict_path[point]
    for _ in range(len(path) - 1, -1, -1):
      if path[_] in main_path:
        break
      extra_path.insert(0, path[_])
    if len(extra_path) > 0:
      dict_extra_path[point] = extra_path
  return dict_extra_path


def MazeAnalysis(maze, alg):
  size = maze.get_size()
  end_point = maze.get_end_point()
  list_point = maze.get_list_point()
  list_consider = [(i, j) for i in range(size[0]) for j in range(size[1]) if list_point[i][j] != 0 or (i,j) == end_point]
  dict_path, path_bot_go = FindPath(maze, list_consider, alg)
  return dict_path, path_bot_go

def Optimal_solution(maze, alg):
  dict_path, path_bot_go = MazeAnalysis(maze, alg)
  main_path = dict_path[maze.get_end_point()]
  list_point = maze.get_list_point()
  alley = TakeExtraPath(dict_path, main_path)
  current_best_road = main_path[:]
  sum_point = sum([list_point[x][y] for x, y in main_path])
  step = len(main_path) - 1
  highest_result = sum_point / step
  all_info_alleys = TakeInfoAlley(list_point, alley, highest_result)
  while True:
    old_len = len(current_best_road)
    current_best_road, sum_point, step, highest_result = ExpandNode(list_point, dict_path, current_best_road, sum_point, step, highest_result, all_info_alleys)
    if len(current_best_road) == old_len:
      break
  full_step = PathAllPoint(maze, main_path, current_best_road)
  return sum_point, current_best_road, step, full_step, path_bot_go, main_path

def ExpandNode(list_point, dict_path, current_best_road, sum_point, step, highest_result, all_info_alleys):
  if len(all_info_alleys) == 0:
    return (current_best_road, sum_point, step, highest_result)
  best_alley = BestGainAlley(all_info_alleys, highest_result)
  if best_alley == []:
    return (current_best_road, sum_point, step, highest_result)
  sum_point += best_alley[1]
  step += best_alley[2]
  highest_result = sum_point/step
  current_best_road = list(set(current_best_road + best_alley[3]))
  d = {}
  for point in best_alley[4]:
    d[point] = dict_path[point]
  new_alley = TakeExtraPath(d, current_best_road)
  all_info_alleys.extend(TakeInfoAlley(list_point, new_alley, highest_result))
  return (current_best_road, sum_point, step, highest_result)

def BestGainAlley(list_info_alleys, highest_result):
  max_in_alley = 0
  list_remove = []
  best_alley = []
  for info in list_info_alleys:
    if info[0] > max_in_alley and info[0] > highest_result:
      best_alley = info
      max_in_alley = info[0]
    elif info[0] <= highest_result:
      list_remove.append(info)
  if best_alley != []:
    list_info_alleys.remove(best_alley)
  for _ in list_remove:
    list_info_alleys.remove(_)
  return best_alley

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

def TakeInfoAlley(list_point, dict_extra_path, highest_result):
  info_all_alleys = Find_Subset(dict_extra_path)
  res = []
  for inp in info_all_alleys:
    t1 = time.time()
    best_in_alley = OptimizeBackTracking(inp, dict_extra_path, list_point)
    t2 = time.time()
    if t2 - t1 > 0.5:
      print("OLD", t2 - t1)
    t1 = time.time()
    test1 = OptimizeBackTracking1(inp, dict_extra_path, list_point)
    t2 = time.time()
    if t2 - t1 > 0.5:
      print("NEW", t2 - t1)
    if test1[1:3] != best_in_alley[1:3]:
      print(test1[1:3])
      print(best_in_alley[1:3])

    if best_in_alley[0] > highest_result:
      res.append(best_in_alley)
  return res

def Calculate(point_add, old_info, dict_path, dict_prev, list_point):
  old_all_cell = old_info[2]
  score = old_info[1] + sum(list_point[x][y] for x, y in dict_prev[point_add] - old_all_cell)
  all_cell = old_all_cell.union(dict_path[point_add])
  formula = score / (2*len(all_cell))
  return (formula, score, all_cell)

def OptimizeBackTracking(inp, dict_extra_path, list_point):
  l_key, l_value = [], []
  all = list(inp.keys())
  best = (0,0,set())
  l_intersect, d_path, d_prev = {}, {}, {}
  for i in range(len(all)):
    point = all[i]
    d_path[point] = set(dict_extra_path[point])
    d_prev[point] = set(inp[point][1])
    info = Calculate(point, (0,0,set()), d_path, d_prev, list_point)
    st = set(all[:i]) - set(inp[point][0]) - set(inp[point][1])
    if len(st) != 0:
      l_key.append(info)
      l_value.append(st)
    l_intersect[point] = st
    if info[0] > best[0]:
      best = info 
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
      if new_info[0] > best[0]:
        best = new_info
    
  formula, score, all_cell = best
  step = 2*len(all_cell)
  point_left_in_alley = list(set(all) - all_cell)
  all_cell = list(all_cell)
  return (formula, score, step, all_cell, point_left_in_alley)


############################# TEST #######################################
def Calculate1(point_add, old_info, dict_path, dict_prev, list_point):
  old_all_cell = old_info[2]
  score = old_info[1] + sum(list_point[x][y] for x, y in dict_prev[point_add] - old_all_cell)
  all_cell = old_all_cell.union(dict_path[point_add])
  formula = score / (2*len(all_cell))
  return (formula, score, all_cell, old_info[3])

def SortPoint(inp, dict_extra_path, list_point):
  all_cell = []
  for point in inp:
    all_cell += dict_extra_path[point]
  all_cell = list(set(all_cell))
  dict_score_div_step = {}
  for point in inp:
    step = 2
    reverse = dict_extra_path[point][::-1]
    for coordinate in reverse:
      if coordinate != point: 
        if (coordinate in inp or len(DimRightRoad(coordinate, [], all_cell)) > 2):
          break
        step += 2
    dict_score_div_step[point] = list_point[point[0]][point[1]] / step
  return dict_score_div_step, sorted(list(inp), key = lambda x: dict_score_div_step[x])
    
def OptimizeBackTracking1(inp, dict_extra_path, list_point):
  l_key, l_value = [], []
  dict_score_div_step, all = SortPoint(inp, dict_extra_path, list_point)
  best = (0,0,set(), tuple())
  l_intersect, d_path, d_prev = {}, {}, {}
  for i in range(len(all)):
    point = all[i]
    d_path[point] = set(dict_extra_path[point])
    d_prev[point] = set(inp[point][1])
    info = Calculate1(point, (0,0,set(),point), d_path, d_prev, list_point)
    st = set(all[i+1:]) - set(inp[point][0]) - set(inp[point][1])
    if len(st) != 0:
      l_key.append(info)
      l_value.append(st)
    l_intersect[point] = st
    if info[0] > best[0]:
      best = info 
  while True:
    if len(l_key) == 0:
      break
    old_info = l_key.pop()
    points = l_value.pop()
    if best[0] > dict_score_div_step[old_info[3]]:
      continue
    for point in points:
      new_info = Calculate1(point, old_info, d_path, d_prev, list_point)
      new_points = set.intersection(points, l_intersect[point])
      if len(new_points) != 0:
        l_key.append(new_info)
        l_value.append(new_points)
      if new_info[0] > best[0]:
        best = new_info
    
  formula, score, all_cell, _ = best
  step = 2*len(all_cell)
  point_left_in_alley = list(set(all) - all_cell)
  all_cell = list(all_cell)
  return (formula, score, step, all_cell, point_left_in_alley)