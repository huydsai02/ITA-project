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
  relation_each_point, _ = Find_Subset(dict_extra_path, enumerate=True)
  l_key, l_value = [], []
  all = list(dict_extra_path.keys())
  l_intersect, d_prev = {}, {}
  sum_point_main = sum(list_point[x][y] for x, y in main_path)
  step_main = len(main_path) - 1
  best = (sum_point_main/step_main, sum_point_main, step_main, set(main_path))

  for i in range(len(all)):
    point = all[i]
    d_prev[point] = set(relation_each_point[point][1])
    info = Calculate(point, best, dict_extra_path, d_prev, list_point)
    st = set(all[:i]) - set(relation_each_point[point][0]) - set(relation_each_point[point][1])
    l_key.append(info)
    l_value.append(st)
    l_intersect[point] = st

  while True:
    if len(l_key) == 0:
      break
    old_info = l_key.pop()
    points = l_value.pop()
    if old_info[0] > best[0]:
      best = old_info
    for point in points:
      new_info = Calculate(point, old_info, dict_extra_path, d_prev, list_point)
      new_points = set.intersection(points, l_intersect[point])
      l_key.append(new_info)
      l_value.append(new_points)
  total_best_score = best[1]
  best_road = list(best[3])
  number_best_step = best[2]
  full_step = PathAllPoint(maze, main_path, best_road)
  return total_best_score, best_road, number_best_step, full_step, path_bot_go

def Calculate(point_add, old_info, dict_path, dict_prev, list_point):
  old_all_cell = old_info[3]
  score = old_info[1] + sum(list_point[x][y] for x, y in dict_prev[point_add] - old_all_cell)
  old_len = len(old_all_cell)
  all_cell = old_all_cell.union(dict_path[point_add])
  step = old_info[2] + 2*(len(all_cell) - old_len)
  formula = score / step
  return (formula, score, step, all_cell)
