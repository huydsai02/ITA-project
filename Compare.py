from CreateMatrix import Maze

############################# Muốn so sánh thì đổi tên Logic hoặc Logic1 bên dưới ############
import Logic as Logic
import UCS as t

_size = (41,41); _num_point = 20; _start = (1,1); _end = (39,39)
alg = "dfs"
i = 0
while True:
  maze = Maze(size = _size, num_point = _num_point, start = _start, end = _end)
  score1, optimal_path1, len_of_best1, op_road1, path_bot_go1 = t.Optimal_solution(maze, alg)
  score, optimal_path, len_of_best, op_road, path_bot_go = Logic.Optimal_solution(maze, alg)
  i += 1
  if i%100 == 0:
    print(i)
  if (set(optimal_path)) != set(optimal_path1) and (score1/len_of_best1) != (score/len_of_best): 
    print(score1, len_of_best1)
    print(score, len_of_best)
    print(i)
    break

