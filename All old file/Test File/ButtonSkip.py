from Button import Button
import GeneralFunction

class ButtonSkip(Button):
  def __init__(self, pos = (0,0), font = 20, size = (170,45), screen = None, bot = None, maze = None):
    super().__init__("next" ,  pos, font, size, screen)
    self.maze = maze
    if bot.dict_path == None:
      size = self.maze.get_size()
      end_point = self.maze.get_end_point()
      list_point = self.maze.get_list_point()
      list_consider = [(i, j) for i in range(size[0]) for j in range(size[1]) if list_point[i][j] != 0 or (i,j) == end_point]
      bot.dict_path, _ = GeneralFunction.DiscoverMaze(self.maze, list_consider, "dfs")

  def click(self,x, y, menu, show_map, bot):
    super().click(x,y)
    a, b = self.full_coor
    if a[0] <= x <= a[1] and b[0] <= y <= b[1]:
      menu.TurnOn()
      show_map.state = True
      bot.InitialBot()
      bot.PathHasGone = []
      for key in bot.dict_path:
        bot.PathHasGone += bot.dict_path[key]
      bot.draw()
