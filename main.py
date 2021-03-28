from drawer import Drawer
from maze import Maze
from indymanager import IndyManager
import cv2
    
print("Hello!\nHow big should the sides of the maze should be:")
n = input()
try:
    n = float(n)
    assert n % 1 == 0 and n > 0
    n = int(n)
except:
    print("The side size must be a positive integer!")
    exit()
print("How many Indys do you want?:")
n_indies = input()
try:
    n_indies = float(n_indies)
    assert n_indies % 1 == 0 and n_indies > 0
    n_indies = int(n_indies)
except:
    print("The side size must be a positive integer!")
    exit()

maze = Maze(n,n)
indy_manager = IndyManager(n, n, maze, n_indies=n_indies)

cell_size = 50 if n < 15 else 20
drawer = Drawer(n,n,2,cell_size,cell_size)

drawable_dict = maze.generate_drawable_dict()
# maze_img = drawer.generate_image(drawable_dict)
# drawer.show_image(maze_img)

indy_manager.run()

drawable_dicts = indy_manager.past_drawable_dicts
for dict_ in drawable_dicts:
    maze_img = drawer.generate_image(dict_)
    cv2.imshow("Maze", maze_img)
    if dict_ == drawable_dicts[-1]:
        k = cv2.waitKey(0)
    else:
        k = cv2.waitKey(100)
    if k == 27:
        break

cv2.destroyAllWindows()
































