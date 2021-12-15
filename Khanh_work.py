from CreateMatrix import *

def FindValidDirection(pos, list_maze, direction = None):
  '''INPUT
        pos: current position of the agent
        list_maze: matrix respresentation of the maze
        direction: the action that the agent took to reach the pos
     OUTPUT
        return directions that do not lead to wall '''  
  steps = [(0,1), (0,-1), (1,0), (-1,0)]
  directions = [] if direction == None else [(-1 * direction[0], -1 * direction[1])]
  for step in steps:
    if list_maze[pos[0] + step[0]][pos[1] + step[1]] != 1:
      if step not in directions:
        directions.append(step)  
  return directions


def Manhattan(x1, x2):
  '''INPUT
        Two different positions x1 and x2
     OUTPUT
        return Manhattan distance between two positions'''
  return abs(x1[0] - x2[0]) + abs(x1[1] - x2[1])


def PriorPop(paths, points= []):
  '''OUTPUT:
         return the path that is closest to a point in points in term of Manhattan distance''' 
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
  '''OUTPUT:
         return every simple path between start position to a point position or end position''' 
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

def DirectionRightRoad(pos, main_path, total_path, direction = None):
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

def Find_Subset(dict_extra_path, enumerate = False):
  extra_points = list(dict_extra_path.keys())
  res = {}
  start_extra = {}
  for point in extra_points:
    # b is the set containing all point positions that the agent has to pass the given point to reach
    descendant_points = [point]
    # c is the set containing all point positions that the agent has to pass to reach the given point
    ascendant_points = [point]
    start_extra[dict_extra_path[point][0]] = start_extra.get(dict_extra_path[point][0],[])
    start_extra[dict_extra_path[point][0]].append(point)
    for other_point in extra_points:
      if point in dict_extra_path[other_point]:
          descendant_points.append(other_point)
      if other_point in dict_extra_path[point]:
          ascendant_points.append(other_point)
    descendant_points = list(set(descendant_points))
    ascendant_points = list(set(ascendant_points))
    res[point] = [descendant_points[:],ascendant_points[:]]
  same_extra = []
  for point in start_extra:
    temp = {}
    for other_point in start_extra[point]:
      temp[other_point] = res[other_point]
    same_extra.append(temp)
  if enumerate:
    return res, same_extra
  return same_extra    

def PathAllPoint(maze, main_path, total_path):
  x, y = maze.get_start_point()
  points = list(set(total_path))
  positions = [(x, y)]
  directions = {}
  directions[(x, y)] = DirectionRightRoad((x,y), main_path, total_path)
  path_bot_go = []
  while True:
    if (x, y) in points:
      points.remove((x, y))
    if (x, y) == maze.get_end_point() and len(points) == 0:
      path_bot_go.append([(x,y), [()]])
      return path_bot_go
    if len(directions[positions[-1]]) == 0:
      positions.pop()
      x, y = positions[-1]
    else:
      direction = directions[(x,y)].pop()
      path_bot_go.append([(x,y), [direction]])
      x += direction[0]
      y += direction[1]
      directions[(x,y)] = directions.get((x,y), DirectionRightRoad((x,y), main_path, total_path, direction))
      if (x, y) not in positions:
        positions.append((x, y))