from drawer import Drawer
from maze import Maze


n = 3

maze = Maze(n,n)

drawer = Drawer(n,n,3,250,250)

maze_img = drawer.generate_image(maze.maze)
drawer.show_image(maze_img)

# cells = {(row,col):"unknown" for row in range(n) for col in range(3)}
# cells[(0,0)] = "indy"
# cells[(1,1)] = "wall"
# cells[(2,2)] = "available"

# img = drawer.generate_image(cells)
# drawer.show_image(img, wait_time=1000)































