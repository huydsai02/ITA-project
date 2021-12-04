from CreateMatrix import *

########################### Khánh ###################################
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
  # lấy cái object maze, points là tọa độ các ô có điểm và điểm kết thúc, alg là thuật toán
  # trả ra là 1 cái dict chứa đường đi từ điểm đầu đến các điểm nằm trong points và cái path_bot_go (ko quan trọng)
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
  # d là dict_extra_path vừa nãy
 # a: a b c d e f g 
 # d: d e f g
 # tập b sẽ gồm b = []
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

def FindDimensionIsPath(coor, main_path, total_path, p = None):
  #Totalpath là danh sách tất cả các tọa độ trong 1 đường đi có nhánh từ điểm đầu đến cuối

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
  # Totalpath là danh sách tất cả các tọa độ trong 1 đường đi có nhánh từ điểm đầu đến cuối
  # Trả về đường đi ngắn nhất mà qua tất cả các điểm đặc biệt
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

###########################################################################
    

############################################## An #############################
def MazeAnalysis(maze, alg):
  # Lấy cái object maze và thuật toán.
  # Trả về cái main_path, dict_extra_path 
  size = maze.get_size()
  end_point = maze.get_end_point()
  list_point = maze.get_list_point()
  list_consider = [(i, j) for i in range(size[0]) for j in range(size[1]) if list_point[i][j] != 0 or (i,j) == end_point]
  # Là tọa độ những ô có điểm và điểm kết thúc
  dict_path, path_bot_go = FindPath(maze, list_consider, alg)
  main_path = dict_path[end_point]
  dict_extra_path = {}
  # Đường phụ cắt main_path
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
  max = -1
  full_info, same_extra = Find_Subset(dict_extra_path)
  new_inp = []
  for inp in same_extra:
    new_inp.append(FullSituation(inp))
  list_subset = CombineList(new_inp)
  sum_point_main = sum([list_point[x][y] for x, y in main_path])
  print(len(list_subset))  
  for subset in list_subset:
    all_extra_path = []
    score_in_extra = []
    for coordinate in list(subset):      
      extra_path = dict_extra_path[coordinate]
      all_extra_path += extra_path
      score_in_extra += full_info[coordinate][1]
    score = sum_point_main + sum([list_point[x][y] for x, y in list(set(score_in_extra))])
    step = len(main_path) + 2*len(set(all_extra_path)) - 1
    formula = score / step
    if formula > max:
      total_path = list(set(main_path + all_extra_path))
      op = (score, total_path, step)
      max = formula
      count = 1
    elif formula == max:
      count += 1
  total_best_score, best_road, leng = op
  full_step = FindOptimalPath(maze, main_path, best_road)
  print("Number of result:", count)
  return total_best_score, best_road, leng, full_step, path_bot_go, main_path

###########################################################################





######################################### Nhật ##############################
def del_relate_info(l1, d):
  return list(set(l1) - set(d[0] + d[1]))

def FullSituation(inp):
  # inp sẽ là cái element của list same_extra
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
  # inp sẽ là cái element của list same_extra
  # res là kết quả
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

def CombineList(l):
  # l sẽ bao gồm các list cần gộp vào với nhau theo kiểu từng phần tử 1
  # VD: l: [[[1],[2]], [[3],[4],[5]]]
  # đầu ra là [[1,3],[1,4], [1,5], [2,3], [2,4], [2,5]]
  lf = []
  ln = len(l)
  if ln == 1:
    return [i[:] for i in l[0]]
  elif ln < 1:
    return [[]]
  cl = CombineList(l[:ln-1])
  for i in l[-1]:
    for j in cl:
      lf.append(j+i)
  return lf
