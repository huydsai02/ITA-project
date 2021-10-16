import numpy as np
import math
from CreateMatrix import *

def CreateMaze(): #return [maze, xs, ys, xf,yf]
    maze = Maze()
    maze.CreateMaze()
    return maze

    
def IsLogical(maze, path):
    xs, ys = maze.get_start_point()
    list_maze = maze.get_list_maze()
    x = path.count('R') - path.count('L') + xs
    y = path.count('D') - path.count('U') + ys
    if x < 0 or x >= len(list_maze[0]):
        return False
    elif y < 0 or y>= len(list_maze):
        return False
    elif list_maze[y][x] == 1:
        return False
    return True

def IsDone(maze, solution):
    xs, ys = maze.get_start_point()
    xf, yf = maze.get_end_point()
    x = solution.count('R') - solution.count('L') + xs
    y = solution.count('D') - solution.count('U') + ys    
    if (x, y) == (xf, yf):
        return True
    return False

def IsNotLoop(maze, path):
    lst = [0]
    c = 0
    for i in path:
        if i == 'L':
            c+=1
        elif i == 'R':
            c-=1
        elif i == 'D':
            c+=math.pi
        elif i == 'U':
            c-=math.pi
        if c in lst:
            return False
        else:
            lst.append(c)
    return True        

def FindPath(maze):
    paths = ['']
    choices = ['L', 'R', 'U', 'D']
    solutions = []
    step = 0
    num0 = sum(i.count(0) for i in maze.get_list_maze())
    while True:
        temp = paths[:]
        paths = []
        for path in temp:
            for choice in choices:
                npath = path + choice
                if IsLogical(maze, npath) and IsNotLoop(maze, path):
                    if 'DU' not in npath and 'UD' not in npath and 'RL' not in npath and 'LR' not in npath:#or get some point
                        paths.append(npath)
                        if IsDone(maze, npath):
                            solutions.append(npath)
                            # print(npath)
        step += 1
        if step > 2*num0:
            return solutions
    return 'not solvable'



if __name__ == '__main__':
    b = CreateMaze()
    print(FindPath(b))

    # maze = CreateMaze()
    # print(IsLogical(maze, 'L'))
