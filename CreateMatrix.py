import random
from random import randint

class Maze(object):
  def __init__(self):
    
    # self.n là kích thước của mê cung
    self.n = 10
    self.matrix = [[0 if (i * j) % 2 == 0 else 1 for i in range(self.n)] for j in range(self.n)]
    self.start_point = (0, randint(0, self.n - 1))
    self.end_point = (self.n-1, randint(0, self.n - 1))
  
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
    # print(l)
    for a,b in l:
      self.matrix[a][b] = 1

    for i in range(n):
      for j in range(n):
        if (i,j) in r:
          self.matrix[i][j] = 0
          if i == n-1 and (i-1,j) not in r:
            self.matrix[i-1][j] = 1
      
    return self.matrix




  def CreateRoad(self):
    n = self.n
    path = []

    start_point = self.start_point
    end_point = self.end_point

    # Tạo ra những điểm phải đi qua
    if n % 2 == 0:
      cbd = n-2
    else:
      cbd = n-1
    even = [i for i in range(2,cbd,2)]
    point_must_go = [start_point]
    for _ in even:
      r = even[randint(0,len(even) - 1)]
      point_must_go.append((_,r))
    point_must_go.append(end_point)
    # print(point_must_go)
    for i in range(len(point_must_go) - 1):
      s = point_must_go[i]
      e = point_must_go[i+1]
      for j in range(s[0], e[0] + 1):
        path.append((j, s[1]))
      for k in range(min(s[1],e[1]), max(s[1],e[1]) + 1):
        path.append((e[0], k))
    self.path = path
    return self.path

    


    

      


