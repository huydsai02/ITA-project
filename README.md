# CAR IN MAZE
* A car need to travel from the start position to the end position in a maze. While travelling, it can collect some points that are already in the maze. Finally, the car need to finish the route with the highest performance score.
* Description:

  + Application: Our project can be a base to create some maze solver games; give a optimal route for shippers; ...
  + In this project, our team have used some searching algorithms like DFS, BFS, A*, unifrom cost search, enumarate, ...
  + Main challenging: We have spent a large time to solve the problem that is optimizing the performance score based on the formula: Total point collected / Total number of steps to travel the route.
  + In the future, some better heuristic searching might be added.  

## DEMO IMAGES
![Sample Maze](https://github.com/huydsai02/ITA-project/blob/main/img/Screen%20Shot%202021-12-19%20at%2015.52.12.png)
![Sample Maze](https://github.com/huydsai02/ITA-project/blob/main/img/Screen%20Shot%202021-12-19%20at%2015.52.28.png)
![Sample Solution](https://github.com/huydsai02/ITA-project/blob/main/img/Screen%20Shot%202021-12-19%20at%2015.53.10.png)

## DEMO VIDEO
[Sample Video](https://github.com/huydsai02/ITA-project/raw/main/img/Screen%20Recording%202021-12-19%20at%2016.02.07.mp4)

## HOW TO INSTALL AND RUN
Open your termial, go to the address you want to install by the command `cd` + your directory to the address and clone our repository by the command `git clone https://github.com/huydsai02/ITA-project.git` 

## HOW TO USE
Run the file **GUI.py**

## ABOUT FUNCTIONS
* **GeneralFunction.py** 
  * `FindValidDirection(pos, list_maze, direction = None)` recieves `pos` as position of a cell, `list_maze` as matrix form of the maze and return a list valid directions except the inverse of some directions in the argument `direction` which is a list.
  * `Manhattan(x1, x2)` recieves `x1`, `x2` as two positions of two cells and return the Manhattan distance between the two cells. 
  * `PriorPop(paths, points= [])` recieves `paths` as a list of paths in term of possition of its cells, `points` as a list of some cells' possiton, consider `Manhattan(path[-1], point)` for each path in `paths` and each point in `points`, return the path that has the minimal `Manhattan(path[-1], point)` and remove it from `paths`.
  * `DiscoverMaze(maze, points = [], alg= 'dfs')` recieves `maze` as a class object of a maze, `points` as a list of some cells' possiton, `alg` as algorithm  we want to use (`'dfs'` is depth first search, `'bfs'` is breath first search, `'A*'` is A* search) and return a dictionary that each key is element of points, value of that key is the shortest path from start cell to the cell correspond to the key; and return a list that each element is a list contain posstion of a cell we considered while implementing the function and a list of valid directions of that cell at the time we consider the cell.
  * `TakeExtraPath(dict_path, main_path)` recieves `dict_path` as a dictionary (in this project, it is the dictionary returned when implementing `DiscoverMaze(maze, points = [], alg= 'dfs')`), `main_path` as the shortest path from start cell to end cell where each element is position of cell and return a dictionary that each key is the same as key in `dict_path`, value of that key is the same as value in `dict_path` but remove cells in `main_path`.
  * `DirectionRightRoad(pos, main_path, total_path, direction = None)` recieves `pos` as a possition af a cell, `main_path`, `total_path` as paths where each element is position of cell, `direction` as list of directions and return a list of directions that not in `direction` and the cell next to `pos` in that direction in `main_path` or in `total_path`; if `direction` has some elements, add the inverse direction of the first direction in `direction` to `direction`.
  * `Find_Subset(dict_extra_path, enumerate = False)` recieves `dict_extra_path` as a dictionary (in this project, it is the dictionary returned when implementing `TakeExtraPath(dict_path, main_path)`), `enumerate` as a boolean variable and if `enumerate` is equal to `False`, return a list that each element is a dictionary that each key is a key in `dict_extra_path` and  its value is a list containing a list of all keys in `dict_extra_path` that the path from start cell to each of them need to pass the key and a list of keys in `dict_extra_path` that the path from start cell to the key need to pass, and all keys in the dictionary have the same `dict_extra_path[point][0]` where point is a key; if `enumerate` is equal to `True`, return a dictionary that each key is a key in `dict_extra_path` and its value is is a list containing a list of all keys in `dict_extra_path` that the path from start cell to each of them need to pass the key and a list of keys in `dict_extra_path` that the path from start cell to the key need to pass.

* **BruteForce.py**
  * `MazeAnalysis(maze, alg)` recieves `maze` as a class object of a maze, `alg` as algorithm  we want to use (`'dfs'` is depth first search, `'bfs'` is breath first search, `'A*'` is A* search) and return `main_path`, `dict_extra_path` and `path_bot_go` where `dict_path, path_bot_go = DiscoverMaze(maze, list_consider, alg)`, `list_consider` is list of all scores cell and end cell, `dict_extra_path = TakeExtraPath(dict_path, main_path)`.
  * `Calculate(point_add, old_info, dict_path, dict_prev, list_point)` recieves `point_add` as a cell's possition, `old_info` as a list containing information of a path, `dict_path` is dictionary like `dict_path` in `dict_path, path_bot_go = DiscoverMaze(maze, list_consider, alg)`, `dict_prev` is a dictionary like `Find_Subset(dict_extra_path, enumerate = True)`, `list_point` as the matrix form of a maze and return information of the new path that contain the path A having `old_info` and the shortest path from path A to `point_add`.
  * `Optimal_solution(maze, dict_path)` recieves `maze` as a class object of a maze, `dict_path` is dictionary like `dict_path` in `dict_path, path_bot_go = DiscoverMaze(maze, list_consider, alg)` and return information of the best path containing its score, list of all cells in the best path, number of steps to traverse, a list of cells in the best path step by step that you can follow it to solve the maze and a list.

* **Greedy.py**
  * `Calculate(point_add, old_info, dict_path, dict_prev, list_point)` is the same as `Calculate(point_add, old_info, dict_path, dict_prev, list_point)` in **BruteForce.py**
  * `PointScoreDivStep(dict_extra_path, list_point)` recieves `dict_extra_path` as a dictionry like `dict_extra_path = TakeExtraPath(dict_path, main_path)`, `list_point` as the matrix form of a maze and return a dictionary that each key is the same as a key in `dict_extra_path`, its value is equal to score in the cell corresponding to the key over number of step to go from that cell to the nearest cell that is a key in `dict_extra_path` or has more than two cells in `DirectionRightRoad(coordinate, [], all_cell)`. 
  * `HighestInOneAlley(inp, dict_extra_path, list_point, dict_score_div_step)` recieves `inp` as a dictionary (in this project, each key is a scored cell in a fixed branch of the main path, its value is the shortest path from the main path to its cell corresponding to its key, `dict_extra_path` as a dictionry like `dict_extra_path = TakeExtraPath(dict_path, main_path)`, `list_point` as the matrix form of a maze, `dict_score_div_step` as a dictionary like the one returned when implementing `PointScoreDivStep(dict_extra_path, list_point)` and return information of the best path in the branch.
  * `TakeHighestEachAlley(list_point, dict_extra_path, dict_score_div_step, highest_result)` recieves `list_point` as the matrix form of a maze, `dict_extra_path` as a dictionry like `dict_extra_path = TakeExtraPath(dict_path, main_path)`, `dict_score_div_step` as a dictionary like the one returned when implementing `PointScoreDivStep(dict_extra_path, list_point)`, `highest_result` as a real number and return a list of `HighestInOneAlley(inp, dict_extra_path, list_point, dict_score_div_step)` for each branch corresponding to the main path in the maze and each branch, its best path must have score/step greater than `highest_result`.
  * `HighestInAllAlley(list_info_alleys, highest_result)` recieves `list_info_alleys` as a list like `TakeHighestEachAlley(list_point, dict_extra_path, dict_score_div_step, highest_result)`, `highest_result` as a real number and return information of the best path in all branches that its score/step is greater than `highest_result`.
  * `ExpandNode(list_point, dict_path, info_optimal_result, all_info_alleys, dict_score_div_step)` recieves `list_point` as the matrix form of a maze, `dict_path` is dictionary like `dict_path` in `dict_path, path_bot_go = DiscoverMaze(maze, list_consider, alg)`, `info_optimal_result` as information of a path, `all_info_alleys` as a list like `TakeHighestEachAlley(list_point, dict_extra_path, dict_score_div_step, highest_result)`, `dict_score_div_step` as a dictionary like the one returned when implementing `PointScoreDivStep(dict_extra_path, list_point)` and return information of the better path compare to the path of `info_optimal_result` or return `info_optimal_result`. 
  * `Optimal_solution(maze, dict_path)` recieves `maze` as class object of a maze, `dict_path` is dictionary like `dict_path` in `dict_path, path_bot_go = DiscoverMaze(maze, list_consider, alg)` and return information of the best path for the maze.

## CREDIT
* Members
  * Nguyễn Thế An
  * Nguyễn Văn Huy
  * Nguyễn Ngọc Khánh
  * Bùi Hồng Nhật
  * Trần Tuấn Phong
* References
  * Professor Muriel Visani's slides




