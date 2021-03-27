from drawer import Drawer
from maze import Maze
from cell import Cell
import numpy as np
from indy import Indy
import cv2

n = 5

maze = Maze(n,n)
indy = Indy(np.random.randint(0,n),np.random.randint(0,n),maze)
drawer = Drawer(n,n,3,50,50)

drawable_dict = maze.generate_drawable_dict()
maze_img = drawer.generate_image(drawable_dict)
drawer.show_image(maze_img)

indy.run()

drawable_dicts = indy.past_drawable_dicts
for dict_ in drawable_dicts:
    maze_img = drawer.generate_image(dict_)
    cv2.imshow("Maze", maze_img)
    k = cv2.waitKey(100)
    # k = cv2.waitKey(0)
    if k == 27:
        break

cv2.destroyAllWindows()
































