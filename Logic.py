from GeneralFunction import *
import Nhat as test

############################################## An #############################
def MazeAnalysis(maze, alg):
  # Lấy cái object maze và thuật toán.
  # Trả về cái main_path, dict_extra_path 
  size = maze.get_size()
  end_point = maze.get_end_point()
  list_point = maze.get_list_point()
  list_consider = [(i, j) for i in range(size[0]) for j in range(size[1]) if list_point[i][j] != 0 or (i,j) == end_point]
  # Là tọa độ những ô có điểm và điểm kết thúc
  dict_path, path_bot_go = DiscoverMaze(maze, list_consider, alg)
  main_path = dict_path[end_point]
  dict_extra_path = TakeExtraPath(dict_path, main_path)
  return main_path, dict_extra_path, path_bot_go
  
def Optimal_solution(maze, alg):
  list_point = maze.get_list_point()
  main_path, dict_extra_path, path_bot_go = MazeAnalysis(maze, alg)
  max = -1
  full_info, same_extra = Find_Subset(dict_extra_path, enumerate = True)
  new_inp = []
  for inp in same_extra:
    new_inp.append(test.FullSituation(inp))
  list_subset = test.Cartesian_product(new_inp)
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
  full_step = PathAllPoint(maze, main_path, best_road)
  print("Number of result:", count)
  return total_best_score, best_road, leng, full_step, path_bot_go

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
