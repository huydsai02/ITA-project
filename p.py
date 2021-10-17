import numpy as np
import math
from CreateMatrix import *

def CreateMaze(size = 10): #return [maze, xs, ys, xf,yf]
    maze = Maze(size)
    return maze

    
def IsLogical(maze, path):
    xs, ys = maze.get_start_point()
    list_maze = maze.get_list_maze()
    size = maze.get_size()
    x = path.count('R') - path.count('L') + xs
    y = path.count('D') - path.count('U') + ys
    if x < 0 or x >= size:
        return False
    elif y < 0 or y >= size:
        return False
    elif list_maze[x][y] == 1:
        return False
    return True

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

def IsSolution(maze, solution):
    xs, ys = maze.get_start_point()
    xf, yf = maze.get_end_point()
    x = solution.count('R') - solution.count('L') + xs
    y = solution.count('D') - solution.count('U') + ys    
    if (x, y) == (xf, yf):
        return True
    return False

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
                        if IsSolution(maze, npath):
                            solutions.append(npath)
                        else:
                            paths.append(npath)
        step += 1
        if step > 2*num0:
            return solutions
    return 'not solvable'

def FindCoordinatePath(maze, solutions):
    s = maze.get_start_point()
    translate = {"L":(-1,0), "R":(1,0), "U":(0,-1), "D":(0,1)}
    all_path = []
    for solution in solutions:
        ns = (s[0], s[1])
        path = [ns]
        for c in solution:
            step = translate[c]
            ns = (ns[0] + step[0], ns[1] + step[1])
            path.append(ns)
        all_path.append(path)
    
    return all_path

def Optimal_result(maze, paths):
    highest_score = 0
    for path in paths:
        score = 0
        for coor in path:
            score += maze.get_list_point()[coor[0]][coor[1]]
        final_score = score / len(path)
        if final_score > highest_score:
            highest_score = final_score
            optimal_path = path
    return (highest_score, optimal_path)

            

if __name__ == '__main__':
    b = CreateMaze(6)
    arr = np.array(b.get_list_maze())
    a = arr.T
    s = FindPath(b)
    p = FindCoordinatePath(b,s)
    r = Optimal_result(b, p)
    
    print(a)
    print(s)

    print(arr)
    print(p)
    
    print(list(zip(s,p)))
    print(r)
