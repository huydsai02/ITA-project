import random
from random import randint

class Maze(object):
  def __init__(self, size = (10,10), have_path = False, hard = 4, create_way = 1):
    # self.size là kích thước của mê cung, vị trí thứ nhất là chiều ngang mê cung, vị trí thứ hai là chiều dọc mê cung
    self.size = size
    self.matrix = self.CreateMaze(have_path, hard, create_way)
    self.list_point = self.Create_list_point(num = int(self.get_size()[0] * self.get_size()[1] / 10))
    self.add_brick_outside()
    self.Set_start_end_in_matrix()


  def CreateMaze(self, have_path = False, hard = 4, create_way = 1):
    ####### Tạo ra một ma trận 0,1 với 1 là tường
    size = self.get_size()
    self.matrix = [[0] * size[1] for _ in range(size[0])]

    if create_way == 1:
      path = []

      if hard > min(size) or hard < 2:
        hard = 4

      if have_path == True: 
        self.point_have_to_go(n = hard)
        path = self.path_through_point()
        
      # Tạo ma trận nhị phân
      for i in range(1,size[0],2):
        for j in range(1,size[1],2):
          self.matrix[i][j] = 1
          r = randint(0,1)
          if (i, j-1) in path and (i-1, j) in path:
            continue
          elif (i, j-1) in path:
            self.matrix[i-1][j] = 1
          elif (i-1, j) in path:
            self.matrix[i][j-1] = 1
          elif r == 1:
            self.matrix[i-1][j] = 1
          elif r == 0:
            self.matrix[i][j-1] = 1
      
      if size[0] % 2 == 1:
        for i in range(1, size[1], 2):
          self.matrix[size[0] - 1][i] = randint(0,1)
      
      if size[1] % 2 == 1:
        for i in range(1, size[0], 2):
          self.matrix[i][size[1] - 1] = randint(0,1)

      # Tạo điểm bắt đầu
      if have_path == False:
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
    
    elif create_way == 2:
      if have_path == False:
        for i in range(1,size[0],2):
          for j in range(1,size[1],2):
            self.matrix[i][j] = 1
            r = randint(0,1)
            if r == 1:
              self.matrix[i-1][j] = 1
            elif r == 0:
              self.matrix[i][j-1] = 1

        if size[0] % 2 == 1:
          for i in range(1, size[1], 2):
            self.matrix[size[0] - 1][i] = randint(0,1)
      
        if size[1] % 2 == 1:
          for i in range(1, size[0], 2):
            self.matrix[i][size[1] - 1] = randint(0,1)

      elif have_path == True:
        for i in range(2,size[0],2):
          for j in range(2,size[1],2):
            self.matrix[i-1][j-1] = 1
            r = randint(0,1)
            if r == 1:
              self.matrix[i-1][j] = 1
            elif r == 0:
              self.matrix[i][j-1] = 1

        if size[0] % 2 == 0:
          for i in range(2, size[1], 2):
            self.matrix[size[0] - 1][i] = randint(0,1)
            self.matrix[size[0] - 1][i-1] = 1
        
        if size[1] % 2 == 0:
          for j in range(2, size[0], 2):
            self.matrix[j - 1][size[1] - 1] = 1
            self.matrix[j][size[1] - 1] = randint(0,1)
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

    
    self.Create_list_point()
    
    return self.matrix
  
  def add_brick_outside(self):
    matrix = self.get_list_maze()
    size = self.get_size()
    list_point = self.get_list_point()
    
    new_list_point = [[0 for i in range(size[1] + 2)] for j in range(size[0] + 2)]
    new_matrix = [[1 for k in range(size[1] + 2)] for h in range(size[0] + 2)]
    for i in range(1, size[0] + 1):
      for j in range(1, size[1] + 1):
        new_matrix[i][j] = matrix[i-1][j-1]
        new_list_point[i][j] = list_point[i-1][j-1]
    
    s = self.get_start_point()
    e = self.get_end_point()
    
    self.set_start_point((s[0]+1,s[1]+1))
    self.set_end_point((e[0]+1,e[1]+1))

    self.set_list_maze(new_matrix)
    self.set_list_point(new_list_point)
    self.set_size((size[0] + 2, size[1] + 2))
    
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
  

  def point_have_to_go(self, n = 5):
    size = self.get_size()
    points = []
    while len(points) <= n:
      a = randint(1, int(size[0]/2 - 1))
      b = randint(1, int(size[1]/2 - 1))
      s = (2*a,2*b)
      if s not in points:
        points.append(s)
    maxs = 0
    for i in range(len(points)-1):
      for j in range(i + 1, len(points)):
        f = points[i]
        t = points[j]
        cal = (f[0] - t[0])**2 + (f[1] - t[1])**2
        if cal > maxs:
          maxs = cal
          st = points[i]
          en = points[j]

    self.set_start_point(st)
    self.set_end_point(en)
    self.points = points
    return self.points

  def path_through_point(self):
    size = self.get_size()
    points = self.points
    path = []
    for i in range(1, len(points)):
      s = points[i-1]
      e = points[i]
      for j in range(min(s[0], e[0]), max(s[0], e[0]) + 1):
        path.append((j, s[1]))
      for k in range(min(s[1], e[1]), max(s[1],e[1]) + 1):
        path.append((e[0], k))
    self.path = path
    return self.path

    
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







  

  


