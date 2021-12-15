from GeneralFunction import *
    
def MazeAnalysis(maze, alg):
  size = maze.get_size()
  end_point = maze.get_end_point()
  list_point = maze.get_list_point()
  list_consider = [(i, j) for i in range(size[0]) for j in range(size[1]) if list_point[i][j] != 0 or (i,j) == end_point]
  dict_path, path_bot_go = DiscoverMaze(maze, list_consider, alg)
  main_path = dict_path[end_point]
  dict_extra_path = TakeExtraPath(dict_path, main_path)
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
  full_step = PathAllPoint(maze, main_path, best_road)
  return total_best_score, best_road, number_best_step, full_step, path_bot_go

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