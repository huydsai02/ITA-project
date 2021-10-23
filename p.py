import numpy as np
import math
from CreateMatrix import *

def LogicCheck(maze, path, s_point):#Liệu bước đi có hợp lý ko
    xs, ys = s_point
    list_maze = maze.get_list_maze()
    size = maze.get_size()
    x = path.count('R') - path.count('L') + xs
    y = path.count('D') - path.count('U') + ys
    if x < 0 or x >= size[0]:
        return False
    elif y < 0 or y >= size[1]:
        return False
    elif list_maze[x][y] == 1:
        return False
    return True

def LoopCheck(path, s_point):#path có đi vòng tại điểm cuối ko, nếu có trả về điểm lặp của loop
    path = PathConvert(path, s_point)
    if path.count(path[-1]) == 1:
        return False
    return True

def EndCheck(solution, s_point, e_point):#liệu path đã đến đích chưa
    xs, ys = s_point
    xf, yf = e_point
    x = solution.count('R') - solution.count('L') + xs
    y = solution.count('D') - solution.count('U') + ys    
    if (x, y) == (xf, yf):
        return True
    return False

def PathConvert(path, s_point):#chuyển từ dãy các bc đi sang toạ độ xe
    xt, yt = s_point
    lst_step = [(xt, yt)]
    for step in path:
        if step == 'U':
            yt-= 1
        elif step =='D':
            yt+= 1
        elif step =='L':
            xt-= 1
        elif step =='R':
            xt+= 1
        lst_step.append((xt, yt))
    return lst_step

def Manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] + p2[1])

def PriorPop(maze, paths, s_point, e_point):
    c = 4 * sum(maze.get_size())
    Ppath = ''
    for path in paths:
        copath = PathConvert(path, s_point)
        node = copath[-1]
        if Manhattan(node, e_point) < c:
            c = Manhattan(node, e_point)
            Ppath = path
    paths.remove(Ppath)
    return Ppath



def ShortestPath(maze, s_point, e_point):#thuật toán để tìm tất cả path tới đích
    paths = ['']
    choices = ['R', 'L', 'D', 'U']
    dic = {'': 0}
    while len(paths) > 0:
        out = PriorPop(maze, paths, s_point, e_point)
        for choice in choices:
            npath = out + choice
            if LogicCheck(maze, npath, s_point):
                if not LoopCheck(npath, s_point):
                    if EndCheck(npath, s_point, e_point):
                        return npath
                    paths.append(npath)
    return False

def ConnectedNode(maze, point):
    start = maze.get_start_point()
    end = maze.get_end_point()
    size = maze.get_size()
    list_point = maze.get_list_point()
    list_node = [start, end]
    connect = []
    for i in range(size[0]):
        for j in range(size[1]):
            if list_point[i][j] > 0:
                list_node.append((i, j)) 
    for i in list_node:
        if ShortestPath(maze, point, i):
            connect.append(i)
    return connect

def PointCollected(maze, path, s_point):
    list_point = maze.get_list_point()
    sum_p = 0
    lst = [s_point]
    for (x, y) in PathConvert(path, s_point):
        if list_point[x][y] > 0 and (x, y) not in lst:
            lst.append((x,y))
            sum_p+=list_point[x][y]
    return sum_p, lst

def PathScore(maze, path, s_point):
    return PointCollected(maze, path, s_point)[0] / len(path)
        
def ExpandNode(maze, node, l, ln):
    lst = []
    for point in l:
        if point not in ln:
            path = ShortestPath(maze, node, point)
            if len(path):  
                lst.append((path, point))
    return lst

def PriorityPop(maze, list, listT, root):
    c = 0
    node = root
    Tpath = ('', node)
    for (path, node) in list:
        if len(path) > 0:
            temp = PathConvert(path, root)[-1]
            if PathScore(maze, path, root) > c and listT.count(temp) == 0:
                c = PathScore(maze, path, root)
                node = temp
                Tpath = (path, node)
    list.remove(Tpath)
    return Tpath

def BestPath(maze):
    start = maze.get_start_point()
    end = maze.get_end_point()
    size = maze.get_size()
    list_point = maze.get_list_point()
    list_node = [start, end]
    Tpath = ('', start)
    listP = [Tpath]
    listT = []
    step = 0
    for i in range(size[0]):
        for j in range(size[1]):
            if list_point[i][j] > 0:
                list_node.append((i, j))
    while True:
        poppath, Tnode = PriorityPop(maze, listP, listT, start)
        listT.append(Tnode)
        pointcollect = PointCollected(maze, poppath, start)[1]
        if Tnode == end:
            return poppath, PointCollected(maze, poppath, start)[0] / len(poppath), len(poppath)
        for pair in ExpandNode(maze, Tnode, list_node, listT):
            if listP.count((poppath + pair[0], pair[1])) == 0 and pointcollect.count(pair[1]) == 0:
                listP.append((poppath + pair[0], pair[1]))
        print(step, Tnode)
        step+=1

            
if __name__ == '__main__':
# size lấy vào kích cỡ mê cung với tham số thứ nhất là số ô ngang mê cung, tham số thứ 2 là số ô dọc mê cung
    # Nếu đưa về list python thì tham số thứ nhất là số hàng, tham số thứ 2 là số cột
    width, height = (30, 30)
    maze_info = Maze(size = (width, height), num_point=20)
    maze = np.array(maze_info.get_list_maze()).T
    lst_point = np.array(maze_info.get_list_point()).T

    print(maze)
    print(maze_info.get_start_point(), maze_info.get_end_point())
    print(lst_point)
    print(ShortestPath(maze_info, maze_info.get_start_point(), maze_info.get_end_point()))
    print(BestPath(maze_info)[0])
    print()

