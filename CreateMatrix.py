import random
from random import randint
class Maze(object):
  def __init__(self, size = (11,11), start = (1,1), end = (9,9), matrix = None, num_point = 12):
    # self.size là kích thước của mê cung, vị trí thứ nhất là chiều ngang mê cung, vị trí thứ hai là chiều dọc mê cung
    self.size = size
    self.matrix = self.CreateMaze() if matrix == None else matrix
    self.start_point = start
    self.end_point = end
    self.matrix[start[0]][start[1]] = 2
    self.matrix[end[0]][end[1]] = 3
    self.Create_list_point(num = num_point)

  def CreateMaze(self):
    size = self.get_size()
    a = size[0] if size[0] % 2 == 1 else size[0] + 1
    b = size[1] if size[1] % 2 == 1 else size[1] + 1
    size = self.size = (a,b)

    self.matrix = [[1 if (i*j) % 2 == 0 else 0 for i in range(b)] for j in range(a)]
    n = int(size[0]/2) * int(size[1]/2)
    nv = 1

    # Điểm khởi tạo mê cung
    start_point = (random.choice(range(1, size[0], 2)), random.choice(range(1, size[1], 2)))
    current_cell = start_point
    cell_stack = []
    while nv < n:
      neighbours = self.find_valid_neighbours(current_cell)
      if not neighbours:
        current_cell = cell_stack.pop()
        continue
      step, next_cell = random.choice(neighbours)
      self.knock_down_wall(current_cell, step)
      cell_stack.append(current_cell)
      current_cell = next_cell
      nv += 1
    
    return self.matrix

  def knock_down_wall(self, cell, step):
    # Phá tường mà step đi qua
    self.matrix[cell[0] + int(step[0]/2)][cell[1] + int(step[1]/2)] = 0

  def has_all_walls(self, i, j):
    m = self.get_list_maze()
    if m[i][j] == 0:
      if m[i-1][j] == 1 and m[i+1][j] == 1 and m[i][j-1] == 1 and m[i][j+1] == 1:
        return True
    return False

  def find_valid_neighbours(self, cell):
    neighbors = []
    x, y = cell
    size = self.get_size()
    steps = [(-2,0), (2,0), (0, -2), (0, 2)]
    for step in steps:
      nx = x + step[0]
      ny = y + step[1]
      if 0 <= nx < size[0] and 0 <= ny < size[1]:
        if self.has_all_walls(nx,ny):
          neighbors.append((step,(nx, ny)))
    return neighbors
    
  def Create_list_point(self, num = 10):
    size = self.get_size()
    m = self.get_list_maze()
    self.list_point = [[0 for i in range(size[1])] for j in range(size[0])]
    lst = [(i, j) for i in range(size[0]) for j in range(size[1]) if m[i][j] == 0]
    point_pos = random.sample(lst, num)
    for _ in range(len(point_pos)):
      i, j = point_pos[_]
      if _ != int(num/2):
        self.list_point[i][j] = (i+j)*2
      else:
        self.list_point[i][j] = 10 * (i+j)
    return self.list_point

  def TakeCoordinatePoint(self):
    lp = self.get_list_point()
    size = self.get_size()
    return [(i, j) for i in range(size[0]) for j in range(size[1]) if lp[i][j] != 0]

  def TakeCoordinateRoad(self):
    lm = self.get_list_maze()
    size = self.get_size()
    lr = [(i, j) for i in range(size[0]) for j in range(size[1]) if lm[i][j] != 1]
    lb = [(i, j) for i in range(size[0]) for j in range(size[1]) if lm[i][j] == 1]
    return lr, lb

  def get_list_point(self):
    return self.list_point

  def get_start_point(self):
    return self.start_point
  
  def get_end_point(self):
    return self.end_point

  def get_list_maze(self):
    return self.matrix

  def get_size(self):
    return self.size








  

  


