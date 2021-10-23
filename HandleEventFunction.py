def NextPosition(x, y, step, maze):
  l = maze.get_list_maze()
  lp = maze.get_list_point()
  nx = x + step[0]
  ny = y + step[1]

  while not CanTurn(nx, ny, l) and not LaNgoCut(nx, ny, l) and lp[nx][ny] == 0 and l[nx][ny] == 0:
    nx += step[0]
    ny += step[1]

  return (nx,ny)

def CanTurn(x, y, l):
  check_direction = [[(1,0),(0,1)], [(-1,0),(0,1)], [(1,0),(0,-1)], [(-1,0),(0,-1)]]
  for pair in check_direction:
    count = 0
    for d in pair:
      if l[x + d[0]][y + d[1]] != 1:
        count += 1
    if count == 2:
      return True
  return False

def LaNgoCut(x, y, l):
  check_direction = [[(1,0),(0,1),(0,-1)], [(-1,0),(0,1),(0,-1)], [(1,0),(-1,0),(0,-1)], [(-1,0),(1,0),(0,1)]]
  for pair in check_direction:
    count = 0
    for d in pair:
      if l[x + d[0]][y + d[1]] == 1:
        count += 1
    if count == 3:
      return True
  return False

def FullMaze(func, para, xs, ys, maze):
  size = maze.get_size()
  cr, (square, square), color_road = para
  dim = [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1), (0,0)]
  l = []
  for x,y in dim:
    a = xs + x
    b = ys + y
    l.append((a,b))
  res = [(i,j) for i in range(size[0]) for j in range(size[1]) if (i,j) not in l]
  func(res, (square, square), (0,0,0))

def ShowBotGo(func, para, l, i):
  lis, square, color, radius = para
  if i < len(l):
    consider = l[int(i)]
    point = consider[0]
    dims = consider[1]
    res = []    
    for a,b in dims:
      j = point[0] + a
      k = point[1] + b
      res.append((j,k))
    func(res, square, color, radius)
    return point

def DelElementFromList(coor, points):
  if coor in points:
    new_points = [point for point in points if point != coor]
    points = new_points
  return points

def PathHasGone(list_gone, cr, cb, func, para, coor):
  r, (square, square), color_road, color_brick = para
  cop = list_gone[:]
  r = []
  b = []
  if coor not in cop:
    cop.append(coor)
  for c in list_gone:
    if c in cr:
      r.append(c)
    if c in cb:
      b.append(c)
  func(r, (square, square), color_road)
  func(b, (square, square), color_brick)
  return cop