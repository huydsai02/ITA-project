import random
from random import randint
class Maze(object):
  def __init__(self, size = (11,11)):
    # self.size là kích thước của mê cung, vị trí thứ nhất là chiều ngang mê cung, vị trí thứ hai là chiều dọc mê cung
    self.size = size
    self.matrix = self.CreateMaze()
    self.Create_list_point()

  def CreateMaze(self):
    size = self.get_size()

    if size[0] % 2 == 0:
      a = size[0] + 1
    else:
      a = size[0]
      
    if size[1] % 2 == 0:
      b = size[1] + 1
    else:
      b = size[1]
    size = self.set_size((a,b))

    self.matrix = [[1 if (i*j) % 2 == 0 else 0 for i in range(size[1])] for j in range(size[0])]
    n = int(size[0]/2) * int(size[1]/2)
    nv = 1
    current_cell = (1,1)
    cell_stack = []
    while nv < n:
      neighbours = self.find_valid_neighbours(current_cell)
      if not neighbours:
        current_cell = cell_stack.pop()
        continue
      step, next_cell = random.choice(neighbours)
      self.matrix[current_cell[0] + int(step[0]/2)][current_cell[1] + int(step[1]/2)] = 0
      cell_stack.append(current_cell)
      current_cell = next_cell
      nv += 1
    s = e = [0,0]
    while (s[0] - e[0])**2 + (s[1] - e[1])**2 < min(size)**2:
      # Tạo điểm bắt đầu
      s = [randint(0,size[0] - 1),randint(0, size[1] - 1)]
      while self.matrix[s[0]][s[1]] == 1:
        s = [randint(0,size[0] - 1),randint(0, size[1] - 1)]
      self.set_start_point((s[0],s[1]))

      # Tạo điểm kết thúc
      e = [randint(0,size[0] - 1),randint(0, size[1] - 1)]
      while self.matrix[e[0]][e[1]] == 1 and s != e:
        e = [randint(0,size[0] - 1),randint(0, size[1] - 1)]
      self.set_end_point((e[0],e[1]))
    return self.matrix

  def has_all_walls(self, i, j):
    m = self.get_list_maze()
    size = self.get_size()
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
    
  def Create_list_point(self, num = 10, ranrange= range(4, 8)):
    size = self.get_size()
    m = self.get_list_maze()
    self.list_point = [[0 for i in range(size[1])] for j in range(size[0])]
    lst = [(i, j) for i in range(size[0]) for j in range(size[1]) if m[i][j] == 0]
    point_pos = random.sample(lst, num)
    for i, j in point_pos:
      self.list_point[i][j] = random.choice(ranrange)
    return self.list_point

  def Set_start_end_in_matrix(self):
    s = self.get_start_point()
    e = self.get_end_point()
    self.matrix[s[0]][s[1]] = 2
    self.matrix[e[0]][e[1]] = 3
  
  def get_list_point(self):
    return self.list_point

  def set_list_point(self, x):
    self.list_point = x
    return self.get_list_point()

  def get_start_point(self):
    return self.start_point
  
  def get_end_point(self):
    return self.end_point

  def set_start_point(self,coor):
    self.start_point = coor
    return self.get_start_point()

  def set_end_point(self, coor):
    self.end_point = coor
    return self.get_end_point()

  def get_list_maze(self):
    return self.matrix

  def set_list_maze(self, x):
    self.matrix = x
    return self.get_list_maze()

  def get_size(self):
    return self.size

  def set_size(self, x):
    self.size = x
    return self.get_size()







  

  


