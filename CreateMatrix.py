import random
from random import randint

class Maze(object):
  def __init__(self):
    # self.n là kích thước của mê cung
    self.n = 10
    self.matrix = [[0 if (i * j) % 2 == 0 else 1 for i in range(self.n)] for j in range(self.n)]
    self.start_point = (randint(0, self.n - 1), randint(0, self.n - 1))
    self.end_point = (randint(0, self.n - 1), randint(0, self.n - 1))

  def get_start_point(self):
    return self.start_point
  
  def get_end_point(self):
    return self.end_point
  
  def RandomBrick(self):
    # Tạo ra các bức tường ngẫu nhiên
    list_coordinate = []
    
    # a càng lớn thì càng nhiều gạch và ngược lại (0 < a < 1)
    a = 2/5
    self.brick = int(((self.n)**2) * a)
    self.randomlist = random.sample(range(1, (self.n)**2 - 1) , self.brick)
    for _ in self.randomlist:
      row = int(_ / self.n)
      column = _ % self.n
      list_coordinate.append((row, column))
    # print(list_coordinate)
    return list_coordinate

  def CreateMaze(self):
    # Tạo ra một ma trận 0,1 với 1 là tường
    l = self.RandomBrick()
    r = self.CreateRoad()
    n = self.n

    for a,b in l:
      self.matrix[a][b] = 1

    for i in range(n):
      for j in range(n):
        if (i,j) in r:
          self.matrix[i][j] = 0

    return self.matrix
      

  def CreateRoad(self):

    # Tạo ra 1 con đường để đi từ điểm đầu đến điểm cuối
    n = self.n
    path = []
    
    s = self.start_point
    e = self.end_point

    for i in range( min((s[0], e[0])) , max((s[0],e[0])) + 1):
      path.append((i, s[1]))
    for j in range( min((s[1], e[1])) , max((s[1],e[1])) + 1):
      path.append((e[0], j))
    
    self.path = path
    return self.path





    


    

      


