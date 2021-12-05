def FindValidDimension(coordinate, list_maze, p = None):
  # Return dimension which is not wall. If p != None, the opposite dimension of p will take the first position
  steps = [(0,1), (0,-1), (1,0), (-1,0)]
  res = [] if p == None else [((-1) * p[0], (-1) * p[1])]
  for step in steps:
    if list_maze[coordinate[0] + step[0]][coordinate[1] + step[1]] != 1 and step not in res:
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

def FindPointNeighbor(maze, dict_path):
  list_consider = Arrange(maze, dict_path)
  start = maze.get_start_point()
  main_path = dict_path[maze.get_end_point()]
  dict_neighbor = {start:[]}
  for xs, ys in list_consider[1:]:
    consider_now = (xs, ys)
    dict_neighbor[consider_now] = dict_neighbor.get(consider_now, [])
    length = len(dict_path[consider_now])
    for i in range(1, length):
      li = length - 1 - i
      if dict_path[consider_now][li] in list_consider:
        dict_neighbor[dict_path[consider_now][li]].append(consider_now)
        if consider_now not in main_path:
          dict_neighbor[consider_now].append(dict_path[consider_now][li])
        break
  for xs, ys in list_consider:
    if (xs, ys) not in main_path:
      temp = dict_neighbor[(xs,ys)].pop(0)
      dict_neighbor[(xs,ys)].append(temp)
  return dict_neighbor

def MazeAnalysis(maze):
  size = maze.get_size()
  end_point = maze.get_end_point()
  list_point = maze.get_list_point()
  list_consider = [(i, j) for i in range(size[0]) for j in range(size[1]) if list_point[i][j] != 0 or (i,j) == end_point]
  dict_path, path_bot_go = FindPath(maze, list_consider)
  dict_neighbor = FindPointNeighbor(maze, dict_path)
  return dict_neighbor, path_bot_go, dict_path

def Arrange(maze, dict_path):
  total_path = []
  main_path = dict_path[maze.get_end_point()]
  for point in list(dict_path.keys()):
    total_path += dict_path[point]
  total_path = list(set(total_path))
  full_step = PathAllPoint(maze, main_path, total_path)
  res = []
  for point, dim in full_step:
    if point not in res and (point == maze.get_start_point() or point in list(dict_path.keys())):
      res.append(point)
  return res

def Optimal_solution(maze, alg = "dfs"):
  dict_neighbor, path_bot_go, dict_path = MazeAnalysis(maze)
  main_path = dict_path[maze.get_end_point()]
  best_road, best_step, best_score = VisitNextNeighbor(dict_neighbor, maze, dict_path)
  total_best_score = best_score
  full_step = PathAllPoint(maze, main_path, best_road)
  total_step = best_step
  return total_best_score, best_road, total_step, full_step, path_bot_go, main_path

def VisitNextNeighbor(dict_neighbor, maze, dict_path):
  point = maze.get_start_point()
  points = [point]
  neighbors = dict_neighbor[point][:]
  dims = [neighbors]
  dict_path[point] = []
  end = maze.get_end_point()
  main_path = dict_path[end]
  max_result = 0
  best_path = []
  while True:    
    if len(points) == 0:
      break
    if dims[-1] == []:
      points.pop()
      dims.pop()
      
    else:
      neighbors = dims[-1]
      point = neighbors.pop(0)    
      if point not in points:
        neighbors = dict_neighbor[point][:]
      else:
        li = len(points) - points[::-1].index(point) - 1
        neighbors = dims[li][:]
      
      points.append(point)  
      dims.append(neighbors)

      if point == end:
        total_path = []
        score = 0
        for point in list(set(points)):
          total_path += dict_path[point]
          score += maze.get_list_point()[point[0]][point[1]]
        step = 2*len(set(total_path) - set(main_path)) + len(set(main_path)) - 1
        formula = score/step
        if formula > max_result:
          best_path = list(set(total_path))
          max_result = formula 
          best_step = step   
          best_score = score
  return best_path, best_step, best_score