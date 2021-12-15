from CreateMatrix import *

def FindValidDirection(pos, list_maze, direction = None):
  steps = [(0,1), (0,-1), (1,0), (-1,0)]
  directions = [] if direction == None else [(-1 * direction[0], -1 * direction[1])]
  for step in steps:
    if list_maze[pos[0] + step[0]][pos[1] + step[1]] != 1:
      if step not in directions:
        directions.append(step)  
  return directions


def Manhattan(x1, x2):
  return abs(x1[0] - x2[0]) + abs(x1[1] - x2[1])


def PriorPop(paths, points= []):
  if len(points):
    min_value = float('inf')
    min_path = paths[-1]
    for path in paths:
      temp = min([Manhattan(path[-1], point) + len(path) - 1 for point in points])
      if temp < min_value:
        min_value = temp
        min_path = path
    paths.remove(min_path)
    return min_path
  else:
    return paths.pop(0)


def DiscoverMaze(maze, points = [], alg= 'dfs'):
  xs,ys = maze.get_start_point()
  list_maze = maze.get_list_maze()
  paths = {}
  valid_direction = {}
  valid_direction[(xs, ys)] = FindValidDirection((xs,ys), list_maze)
  path_bot_go = [[(xs,ys), valid_direction[(xs,ys)][:]]]
  if alg == 'dfs':
    subpath = [(xs, ys)]
    x,y = xs,ys
    while len(points) > 0:
      if not valid_direction[subpath[-1]]:
        subpath.pop()
      else:
        directions = valid_direction[(x,y)]
        direction = directions.pop()
        x += direction[0]
        y += direction[1]
        valid_direction[(x,y)] = valid_direction.get((x,y), FindValidDirection((x,y), list_maze, direction))
        path_bot_go.append([(x,y), valid_direction[(x,y)][:]])
        if (x, y) not in subpath:
          subpath.append((x, y))

      if (x, y) in points:
        path = subpath[:]
        paths[(x, y)] = path
        points = [point for point in points if point != (x,y)]
    return paths, path_bot_go
  
  elif alg.lower() == 'A*'.lower():
    subpaths = [[(xs, ys)]]
    while len(points) > 0:
      subpath = PriorPop(subpaths,points)
      (x, y) = subpath[-1]
      if len(valid_direction[(x, y)]):
        for direction in valid_direction[(x, y)]:
          x0, y0 = x + direction[0], y + direction[1]
          subpaths.append(subpath[:] + [(x0,y0)])
          direct0 = FindValidDirection((x0, y0), list_maze, direction)
          direct0.pop(0)
          valid_direction[(x0, y0)] = valid_direction.get((x0, y0), direct0)
          path_bot_go.append([(x0, y0), valid_direction[(x0, y0)][:]])
          
          if (x0, y0) in points:
            paths[(x0, y0)] = subpath[:] + [(x0,y0)]
            points = [point for point in points if point != (x0,y0)]
    return paths, path_bot_go
  
  elif alg == 'bfs':
    subpaths = [[(xs, ys)]]
    while len(points) > 0:
      subpath = subpaths.pop(0)
      (x, y) = subpath[-1]
      if len(valid_direction[(x, y)]):
        for direction in valid_direction[(x, y)]:
          x0, y0 = x + direction[0], y + direction[1]
          subpaths.append(subpath[:] + [(x0,y0)])
          direct0 = FindValidDirection((x0, y0), list_maze, direction)
          direct0.pop(0)
          valid_direction[(x0, y0)] = valid_direction.get((x0, y0), direct0)
          path_bot_go.append([(x0, y0), valid_direction[(x0, y0)][:]])
          
          if (x0, y0) in points:
            paths[(x0, y0)] = subpath[:] + [(x0,y0)]
            points = [point for point in points if point != (x0,y0)]
    return paths, path_bot_go

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
  
######################################### Cần xem xét từ đây ####################################

def Find_Subset(dict_extra_path, enumerate = False):
  extra_points = list(dict_extra_path.keys())
  res = {}
  start_extra = {}
  for point in extra_points:
    # tập b là tập những điểm phải đi qua point mới đến được
    b = [point]
    # tập c là tập những điểm phải đi qua mới đến point được
    c = [point]
    start_extra[dict_extra_path[point][0]] = start_extra.get(dict_extra_path[point][0],[])
    start_extra[dict_extra_path[point][0]].append(point)
    for other_point in extra_points:
      if point in dict_extra_path[other_point]:
          b.append(other_point)
      if other_point in dict_extra_path[point]:
          c.append(other_point)
    b = list(set(b))
    c = list(set(c))
    res[point] = [b[:],c[:]]
  same_extra = []
  for point in start_extra:
    a = {}
    for other_point in start_extra[point]:
      a[other_point] = res[other_point]
    same_extra.append(a)
  if enumerate:
    return res, same_extra
  return same_extra  

def DimRightRoad(pos, main_path, total_path, direction = None): # Là hàm FindDirectionIsPath cũ
  steps = [(0,1), (0,-1), (1,0), (-1,0)]
  directions = []
  if direction != None:
    directions.append((-1 * direction[0], -1 * direction[1]))
  for step in steps:
    if step not in directions and (pos[0] + step[0],pos[1] + step[1]) in main_path:
      directions.append(step)
  for step in steps:
    if step not in directions and (pos[0] + step[0],pos[1] + step[1]) in total_path:
      directions.append(step)
  return directions

def PathAllPoint(maze, main_path, total_path):
  xs, ys = maze.get_start_point()
  points = list(set(total_path))
  coors = [(xs, ys)]
  dims = {}
  dims[(xs, ys)] = DimRightRoad((xs,ys), main_path, total_path)
  path_bot_go = []
  while True:
    if (xs, ys) in points:
      points.remove((xs, ys))
    if (xs, ys) == maze.get_end_point() and len(points) == 0:
      path_bot_go.append([(xs,ys), [()]])
      return path_bot_go
    if len(dims[coors[-1]]) == 0:
      coors.pop()
      xs, ys = coors[-1]
    else:
      dim = dims[(xs,ys)]
      cpath = dim.pop()
      path_bot_go.append([(xs,ys), [cpath]])
      xs += cpath[0]
      ys += cpath[1]
      dims[(xs,ys)] = dims.get((xs,ys), DimRightRoad((xs,ys), main_path, total_path, direction = cpath))
      if (xs, ys) not in coors:
        coors.append((xs, ys))
