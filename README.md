# CAR IN MAZE
* A car need to travel from the start position to the end position in a maze. While travelling, it can collect some points that are already in the maze. Finally, the car need to finish the route with the highest performance score.
* Description:

  + Application: Our project can be a base to create some maze solver games; give a optimal route for shippers; ...
  + In this project, our team have used some searching algorithms like DFS, BFS, A*, unifrom cost search, enumarate, ...
  + Main challenging: We have spent a large time to solve the problem that is optimizing the performance score based on the formula: Total point collected / Total number of steps to travel the route.
  + In the future, some better heuristic searching might be added.  

## DEMO IMAGES
![Maze Sample](https://github.com/huydsai02/ITA-project/blob/main/img/Screen%20Shot%202021-12-19%20at%2015.52.12.png)
![Maze Sample](https://github.com/huydsai02/ITA-project/blob/main/img/Screen%20Shot%202021-12-19%20at%2015.52.28.png)
![Solution Sample](https://github.com/huydsai02/ITA-project/blob/main/img/Screen%20Shot%202021-12-19%20at%2015.53.10.png)

## DEMO VIDEO
[Video Sample (Click to download)](https://github.com/huydsai02/ITA-project/raw/main/img/Screen%20Recording%202021-12-19%20at%2016.02.07.mp4)

## HOW TO INSTALL AND RUN
Open your termial, go to the address you want to install by the command `cd` + your directory to the address and clone our repository by the command `git clone https://github.com/huydsai02/ITA-project.git` 

## HOW TO USE
Run the file **GUI.py**

## ABOUT FUNCTIONS
* <font size="10"> **GeneralFunction.py** </font>
  * `FindValidDirection(pos, list_maze, direction = None)` recieves `pos` as position of a cell, `list_maze` as matrix form of the maze and return a list valid directions except the inverse of some directions in the argument `direction` which is a list.
  * `Manhattan(x1, x2)` recieves `x1`, `x2` as two positions of two cells and return the Manhattan distance between the two cells. 

## CREDIT
* Members
  * Nguyễn Thế An
  * Nguyễn Văn Huy
  * Nguyễn Ngọc Khánh
  * Bùi Hồng Nhật
  * Trần Tuấn Phong
* References

  + Professor Muriel Visani's slides




