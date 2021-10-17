import numpy as np
import math
from CreateMatrix import *

def CreateMaze(size = 10, pro_brick = 2/5, index = 0): # pro_brick: proportion of brick (0 < pro_brick < 1)
    maze = Maze(size, pro_brick)
    maze.test1(index) 
    maze.test2(index)
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

def IsRecievedPoint(maze, path):
    xs, ys = maze.get_start_point()
    x = path.count('R') - path.count('L') + xs
    y = path.count('D') - path.count('U') + ys
    if maze.get_list_point()[x][y] > 0:
        return True
    return False

def IsSolution(maze, solution):
    xs, ys = maze.get_start_point()
    xf, yf = maze.get_end_point()
    x = solution.count('R') - solution.count('L') + xs
    y = solution.count('D') - solution.count('U') + ys    
    if (x, y) == (xf, yf):
        return True
    return False

def PathConvert(maze, path):
    xt, yt = maze.get_start_point()
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
                if IsLogical(maze, npath) and IsNotLoop(maze, npath):
                    if ('DU' not in npath and 'UD' not in npath and 'RL' not in npath and 'LR' not in npath) or IsRecievedPoint(maze, npath):
                        if IsSolution(maze, npath):
                            solutions.append(npath)
                        else:
                            paths.append(npath)
        step += 1
        if step > 2*num0:
            return solutions
    return 'not solvable'

def Optimal_result(maze, solutions):
    highest_score = 0
    best_solution = ''
    for solution in solutions:
        score = 0
        xt, yt = maze.get_start_point()
        for step in solution:
            if step == 'U':
                yt-= 1
            elif step =='D':
                yt+= 1
            elif step =='L':
                xt-= 1
            elif step =='R':
                xt+= 1
            score+= maze.get_list_point()[xt][yt]
        if score/len(solution) >= highest_score:
            highest_score = score/len(solution)
            best_solution = solution
    return highest_score, best_solution, len(best_solution), highest_score*len(best_solution)
            

if __name__ == '__main__':
    maze_info = CreateMaze(10, pro_brick=3/5)
    maze = np.array(maze_info.get_list_maze()).T
    lst_point = np.array(maze_info.get_list_point()).T
    solutions = FindPath(maze_info)
    the_most = Optimal_result(maze_info, solutions)

    print(maze)
    print(maze_info.get_start_point(), maze_info.get_end_point())
    print(solutions)

    print(lst_point)
    print(the_most)
    print('The best solution is', the_most[1], 'with core', the_most[0])

