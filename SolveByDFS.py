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

def FindPointNeighbor(maze, dict_path):
  list_consider = Arrange(maze, dict_path)
  start = maze.get_start_point()
  end = maze.get_end_point()
  main_path = dict_path[end]
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

def MazeAnalysis(maze, alg):
  size = maze.get_size()
  end_point = maze.get_end_point()
  list_point = maze.get_list_point()
  list_consider = [(i, j) for i in range(size[0]) for j in range(size[1]) if list_point[i][j] != 0 or (i,j) == end_point]
  dict_path, path_bot_go = FindPath(maze, list_consider, alg)
  main_path = dict_path[end_point]
  dict_neighbor = FindPointNeighbor(maze, dict_path)
  return dict_neighbor, path_bot_go, dict_path

def Arrange(maze, dict_path):
  total_path = []
  main_path = dict_path[maze.get_end_point()]
  for point in list(dict_path.keys()):
    total_path += dict_path[point]
  total_path = list(set(total_path))
  full_step = FindOptimalPath(maze, main_path, total_path)
  res = []
  for point, dim in full_step:
    if point not in res and (point == maze.get_start_point() or point in list(dict_path.keys())):
      res.append(point)
  return res

def Optimize_solution(maze, alg):
  dict_neighbor, path_bot_go, dict_path = MazeAnalysis(maze, alg)
  main_path = dict_path[maze.get_end_point()]
  xs, ys = maze.get_start_point()
  best_road, best_step, best_score = VisitNextNeighbor((xs,ys), dict_neighbor, maze, dict_path)
  total_best_score = best_score
  full_step = FindOptimalPath(maze, main_path, best_road)
  total_step = best_step
  return total_best_score, best_road, total_step, full_step, path_bot_go, main_path

def VisitNextNeighbor(start, dict_neighbor, maze, dict_path):
  point = start
  points = [point]
  neighbors = dict_neighbor[point][:]
  dims = [neighbors]
  dict_path[start] = []
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
        length = len(points)
        for i in range(length):
          li = length - i - 1
          if points[li] == point:
            break
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