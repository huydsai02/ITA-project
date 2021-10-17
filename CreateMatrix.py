import random
from random import randint

class Maze(object):
  def __init__(self, size = (10,10)):
    # self.size là kích thước của mê cung, vị trí thứ nhất là chiều ngang mê cung, vị trí thứ hai là chiều dọc mê cung
    self.size = size
    self.matrix = self.CreateMaze()
    self.Set_start_end_in_matrix()
    self.list_point = self.Create_list_point()


  def CreateMaze(self):
    ####### Tạo ra một ma trận 0,1 với 1 là tường
    size = self.get_size()
    self.matrix = [[0] * size[1] for _ in range(size[0])]

    # Tạo ma trận nhị phân
    for i in range(1,size[0],2):
      for j in range(1,size[1],2):
        self.matrix[i][j] = 1
        r = randint(0,1)
        if r == 0:
          self.matrix[i][j-1] = 1
        else:
          self.matrix[i-1][j] = 1
    
    if size[0] % 2 == 1:
      for i in range(size[0]):
        if self.matrix[size[0] - 2][i] == 1:
          self.matrix[size[0] - 1][i] = randint(0,1)
    
    if size[1] % 2 == 1:
      for i in range(size[1]):
        if self.matrix[i][size[1] - 2] == 1:
          self.matrix[i][size[1] - 1] = randint(0,1)

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
    
    self.Create_list_point()
    
    return self.matrix
      
  def Create_list_point(self, num= 10, ranrange= range(4, 8)):
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

  def get_size(self):
    return self.size







  

  


