from GeneralFunction import *

def Optimal_solution(maze, dict_path):
  main_path = dict_path[maze.get_end_point()]
  alley = TakeExtraPath(dict_path, main_path)
  list_point = maze.get_list_point()
  dict_score_div_step = PointScoreDivStep(alley, list_point)

  current_best_road = main_path[:]
  sum_point = sum([list_point[x][y] for x, y in main_path])
  step = len(main_path) - 1
  highest_result = sum_point / step
  all_info_alleys = TakeHighestEachAlley(list_point, alley, dict_score_div_step, highest_result)
  info_optimal_result = (current_best_road, sum_point, step, highest_result)
  step_expand = []
  while True:
    old_len = len(info_optimal_result[0])
    step_expand.append(info_optimal_result[:3])
    info_optimal_result = ExpandNode(list_point, dict_path, info_optimal_result, all_info_alleys, dict_score_div_step)
    if len(info_optimal_result[0]) == old_len:
      break
  current_best_road, sum_point, step, highest_result = info_optimal_result
  full_step = PathAllPoint(maze, main_path, current_best_road)
  return sum_point, current_best_road, step, full_step, step_expand

def ExpandNode(list_point, dict_path, info_optimal_result, all_info_alleys, dict_score_div_step):
  if len(all_info_alleys) == 0:
    return info_optimal_result
  current_best_road, sum_point, step, highest_result = info_optimal_result
  best_alley = HighestInAllAlley(all_info_alleys, highest_result)
  if best_alley == []:
    return info_optimal_result
  sum_point += best_alley[1]
  step += best_alley[2]
  highest_result = sum_point/step
  current_best_road = list(set(current_best_road + best_alley[3]))
  d = {}
  for point in best_alley[4]:
    d[point] = dict_path[point]
  new_alley = TakeExtraPath(d, current_best_road)
  all_info_alleys.extend(TakeHighestEachAlley(list_point, new_alley, dict_score_div_step, highest_result))
  return (current_best_road, sum_point, step, highest_result)

def HighestInAllAlley(list_info_alleys, highest_result):
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

def TakeHighestEachAlley(list_point, dict_extra_path, dict_score_div_step, highest_result):
  info_all_alleys = Find_Subset(dict_extra_path)
  res = []
  for inp in info_all_alleys:
    best_in_alley = HighestInOneAlley(inp, dict_extra_path, list_point, dict_score_div_step)
    if best_in_alley[0] > highest_result:
      res.append(best_in_alley)
  return res

def Calculate(point_add, old_info, dict_path, dict_prev, list_point):
  old_all_cell = old_info[2]
  score = old_info[1] + sum(list_point[x][y] for x, y in dict_prev[point_add] - old_all_cell)
  all_cell = old_all_cell.union(dict_path[point_add])
  formula = score / (2*len(all_cell))
  return (formula, score, all_cell, old_info[3])

def PointScoreDivStep(dict_extra_path, list_point):
  all_cell = []
  for point in dict_extra_path:
    all_cell += dict_extra_path[point]
  all_cell = list(set(all_cell))
  dict_score_div_step = {}
  for point in dict_extra_path:
    step = 2
    reverse = dict_extra_path[point][::-1]
    for coordinate in reverse:
      if coordinate != point: 
        if (coordinate in dict_extra_path or len(DirectionRightRoad(coordinate, [], all_cell)) > 2):
          break
        step += 2
    dict_score_div_step[point] = list_point[point[0]][point[1]] / step
  return dict_score_div_step
    
def HighestInOneAlley(inp, dict_extra_path, list_point, dict_score_div_step):
  l_key, l_value = [], []
  all = sorted(list(inp), key = lambda x : dict_score_div_step[x])
  best = (0,0,set(), tuple())
  l_intersect, d_path, d_prev = {}, {}, {}
  for i in range(len(all)):
    point = all[i]
    d_path[point] = set(dict_extra_path[point])
    d_prev[point] = set(inp[point][1])
    info = Calculate(point, (0,0,set(),point), d_path, d_prev, list_point)
    point_can_choose = set(all[i+1:]) - set(inp[point][0]) - set(inp[point][1])
    if len(point_can_choose) != 0:
      l_key.append(info)
      l_value.append(point_can_choose)
    l_intersect[point] = point_can_choose
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
      new_info = Calculate(point, old_info, d_path, d_prev, list_point)
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