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
      # xs, ys = coors[-1]
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
    if len(coors) == 0: ############################ M đã sửa chỗ này, sau xem xét fix bug (Có vẻ đã fix được nhưng cứ xem xét thêm) ########
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
  full_info, same_extra = Find_Subset(diction_road)
  new_inp = []
  for inp in same_extra:
    new_inp.append(FullSituation(inp))
  # print(new_inp)
  list_subset = CombineList(new_inp)
  # print(list_subset)
  sum_point_main = sum([list_point[x][y] for x, y in main_path])
  # print(full_info)
  print(len(list_subset))  
  ############################################Đoạn này chạy chưa nhanh#############
  for subset in list_subset:
    all_extra_path = []
    score_in_extra = []
    for coordinate in list(subset):      
      extra_path = diction_road[coordinate]
      all_extra_path += extra_path
      score_in_extra += full_info[coordinate][1]
    score = sum_point_main + sum([list_point[x][y] for x, y in list(set(score_in_extra))])
    length = len(main_path) + 2*len(set(all_extra_path)) - 1
    formula = score / length
    if formula >= max:
      total_path = list(set(main_path + all_extra_path))
      op = (score, total_path, length)
      max = formula
  #######################################################################################
  total_best_score, best_road, leng = op
  full_step = FindOptimalPath(maze, main_path, best_road)
  print(leng == (len(full_step) - 1))
  return total_best_score, best_road, leng, full_step, path_bot_go, main_path

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

def del_relate_info(l1, d):
  # new_l = []
  # for point in l1:
  #   if point not in d[0] and point not in d[1]:
  #     new_l.append(point)
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

def CombineList(l):
  lf = []
  ln = len(l)
  if ln == 1:
    return [i[:] for i in l[0]]
  for i in l[-1]:
    for j in CombineList(l[:ln-1]):
      j += i
      lf.append(j)
  return lf