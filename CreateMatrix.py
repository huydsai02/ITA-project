import random
from random import randint

class Maze(object):
  def __init__(self, size = 10, pro_brick = 2/5):
    # self.size là kích thước của mê cung
    self.size = size
    self.start_point = (randint(0, self.get_size() - 1), randint(0, self.get_size() - 1))
    self.end_point = (randint(0, self.get_size() - 1), randint(0, self.get_size() - 1))
    self.pro_brick = pro_brick
    self.matrix = self.CreateMaze()
    self.Set_start_end_in_matrix()
    self.list_point = self.Create_list_point()

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
  
  def RandomBrick(self):
    # Tạo ra các bức tường ngẫu nhiên
    list_coordinate = []
    size = self.get_size()
    # a càng lớn thì càng nhiều gạch và ngược lại (0 < a < 1)
    a = self.pro_brick
    self.brick = int(((size)**2) * a)
    self.randomlist = random.sample(range(1, (size)**2 - 1) , self.brick)
    for _ in self.randomlist:
      row = int(_ / size)
      column = _ % size
      list_coordinate.append((row, column))
    # print(list_coordinate)
    self.list_coordinate = list_coordinate
    return list_coordinate

  def CreateMaze(self):
    # Tạo ra một ma trận 0,1 với 1 là tường
    l = self.RandomBrick()
    r = self.CreateRoad()
    n = self.get_size()
    self.matrix = [[0 for i in range(self.size)] for j in range(self.size)]

    for a,b in l:
      self.matrix[a][b] = 1

    for i in range(n):
      for j in range(n):
        if (i,j) in r:
          self.matrix[i][j] = 0

    return self.matrix
      
  def CreateRoad(self):
    # Tạo ra 1 con đường để đi từ điểm đầu đến điểm cuối
    n = self.get_size()
    path = []
    
    s = self.start_point
    e = self.end_point

    for i in range( min((s[0], e[0])) , max((s[0],e[0])) + 1):
      path.append((i, s[1]))
    for j in range( min((s[1], e[1])) , max((s[1],e[1])) + 1):
      path.append((e[0], j))
    
    self.path = path
    return self.path

  def Create_list_point(self):
    size = self.get_size()
    m = self.get_list_maze()
    self.list_point = [[0 for i in range(size)] for j in range(size)]
    for i in range(size):
      for j in range(size):
        if m[i][j] == 0:
          self.list_point[i][j] = randint(20,40)
    return self.list_point

  def test(self, status = True):
    if status:
      size = self.get_size()
      self.matrix = [[1 if (i*j) % 2 != 0 else 0 for i in range(size)] for j in range(size)]
      s = [1,1]
      while (s[0] * s[1]) % 2 == 1:
        s[0] = randint(0, size-1)
        s[1] = randint(0, size-1)

      e = [1,1]
      while (e[0] * e[1]) % 2 == 1 and s != e:
        e[0] = randint(0, size-1)
        e[1] = randint(0, size-1)

      self.set_start_point(tuple(s))
      self.set_end_point(tuple(e))
      self.Set_start_end_in_matrix()
      self.Create_list_point()