import numpy as np
import math
from CreateMatrix import *

def IsLogical(maze, path):#Liệu bước đi có hợp lý ko
    xs, ys = maze.get_start_point()
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
    elif (x, y) == (xs, ys):
        return False
    return True

def HasLoop(maze, path):#path có đi vòng tại điểm cuối ko, nếu có trả về điểm lặp của loop
    path = PathConvert(maze, path)
    if path.count(path[-1]) == 1:
        return [False]
    return [True, len(path) - 1 - path[::-1][1:].index(path[-1])]

def IsConsideredLoop(maze, path):#path có cần xem xét ko, là path mà chỉ quay lại khi đạt đc điểm, nếu có trả về bc mà đạt đc điểm
    if HasLoop(maze, path)[0]:
        lst = PathConvert(maze, path)[HasLoop(maze, path)[1] - 1:]
        if len(lst)%2 == 1:
            n = (len(lst) - 1)//2
            if maze.get_list_point()[lst[n][0]][lst[n][1]] > 0:
                for i in range(n):
                    if lst[i] != lst[len(lst) - i - 1]:
                        return [False]
                return [True, HasLoop(maze, path)[1] + n]
    return [False]

def IsGoodLoop(maze, path):#liệu path cần xem xét đó có tốt ko, VD: '.....UDU' đạt điểm tại bc U là 1 path xấu
    copath = PathConvert(maze, path)
    l = len(copath)
    if IsConsideredLoop(maze, path)[0]:
        n = IsConsideredLoop(maze, path)[1]
        if IsConsideredLoop(maze, path[: n - 1])[0]:
            return False
        elif copath.count(copath[l - 2:]) > 2:
            return False
        return True
    return False
                 
def IsRecievedPoint(maze, path):#liệu path có ăn điểm tại bước cuối ko
    xs, ys = maze.get_start_point()
    x = path.count('R') - path.count('L') + xs
    y = path.count('D') - path.count('U') + ys
    if maze.get_list_point()[x][y] > 0:
        return True
    return False

def IsSolution(maze, solution):#liệu path đã đến đích chưa
    xs, ys = maze.get_start_point()
    xf, yf = maze.get_end_point()
    x = solution.count('R') - solution.count('L') + xs
    y = solution.count('D') - solution.count('U') + ys    
    if (x, y) == (xf, yf):
        return True
    return False

def PathConvert(maze, path):#chuyển từ dãy các bc đi sang toạ độ xe
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

def FindPath(maze):#thuật toán để tìm tất cả path tới đích
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
                if IsLogical(maze, npath):
                    if not HasLoop(maze, npath)[0]:
                        if IsSolution(maze, npath):
                            solutions.append(npath)
                        else:
                            paths.append(npath)
                    elif IsConsideredLoop(maze, npath)[0]:
                        if IsGoodLoop(maze, npath):
                            paths.append(npath)
        step += 1
        if step > 2*num0:
            break
    return solutions



                        
    


def Optimal_result(maze, solutions):#tìm thông tin path có final score cao nhất 
    highest_score = 0
    best_solution = ''
    for solution in solutions:
        score = [[], []]
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
            if (xt, yt) not in score[1]:
                score[0].append(maze.get_list_point()[xt][yt])
                score[1].append((xt, yt))
        score = sum(score[0])
        if score/len(solution) > highest_score:
            highest_score = score/len(solution)
            best_solution = solution
    return highest_score, best_solution, len(best_solution), highest_score*len(best_solution)
            

if __name__ == '__main__':
# size lấy vào kích cỡ mê cung với tham số thứ nhất là số ô ngang mê cung, tham số thứ 2 là số ô dọc mê cung
    # Nếu đưa về list python thì tham số thứ nhất là số hàng, tham số thứ 2 là số cột
    width, height = (19, 19)
    s = (random.choice(range(1,width - 2,2)),random.choice(range(1,height - 2,2)))
    e = (random.choice(range(1,width - 2,2)),random.choice(range(1,height - 2,2)))
    maze_info = Maze(size = (width, height), num_point= 10, start = s, end = e, multi_path = True)
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
