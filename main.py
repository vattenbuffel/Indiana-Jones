from drawer import Drawer
from maze import Maze
from indymanager import IndyManager
import cv2

n = 40

maze = Maze(n,n)
indy_manager = IndyManager(n, n, maze, n_indies=2)
drawer = Drawer(n,n,3,15,15)

drawable_dict = maze.generate_drawable_dict()
maze_img = drawer.generate_image(drawable_dict)
drawer.show_image(maze_img)

indy_manager.run()

drawable_dicts = indy_manager.past_drawable_dicts
for dict_ in drawable_dicts:
    maze_img = drawer.generate_image(dict_)
    cv2.imshow("Maze", maze_img)
    if dict_ == drawable_dicts[-1]:
        k = cv2.waitKey(0)
    else:
        k = cv2.waitKey(10)
    if k == 27:
        break

cv2.destroyAllWindows()
































