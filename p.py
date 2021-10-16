from CreateMatrix import *

def CreateMaze(): #return [maze, xs, ys, xf,yf]
    matrix = Maze()
    maze = matrix.CreateMaze()
    n = matrix.n
    return (matrix, 0, 0, n-1, n-1)
    
def IsLogical(maze, path):
    xs, ys = maze[1], maze[2]
    x = path.count('R') - path.count('L') + xs
    y = path.count('D') - path.count('U') + ys
    if x < 0 or x >= len(maze[0][0]):
        return False
    elif y < 0 or y>= len(maze[0]):
        return False
    elif maze[0][y][x] == 1:
        return False
    return True

def IsDone(maze, solution):
    xs, ys, xf, yf = maze[1], maze[2], maze[3], maze[4]
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
    while True:
        temp = paths[:]
        paths = []
        for path in temp:
            for choice in choices:
                npath = path + choice
                if IsLogical(maze, npath):
                    if 'DU' not in npath and 'UD' not in npath and 'RL' not in npath and 'LR' not in npath:                    
                        paths.append(npath)
                if IsDone(maze, npath):
                    if 'DU' not in npath and 'UD' not in npath and 'RL' not in npath and 'LR' not in npath:
                        solutions.append(npath)
        step += 1
        if step > 100:
            return solutions
    return 'not solvable'



if __name__ == '__main__':
    print(FindPath(CreateMaze()))

    # maze = CreateMaze()
    # print(IsLogical(maze, 'L'))
