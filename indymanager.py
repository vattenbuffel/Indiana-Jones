from cell import Cell
from maze import Maze
from indy import Indy
import numpy as np
try:
    import networkx as nx
except ModuleNotFoundError:
    print("You need to install networkx. Try the command: pip3 install networkx")
    exit(0)

class IndyManager:
    def __init__(self, x_max, y_max, maze:Maze, n_indies = 2):
        self.maze = maze
        self.available_jobs = []
        self.indy_pos_list = []
        self.cells = {location: Cell(*location, "unknown") for location in maze.cells}

        
        self.G = nx.Graph()
        self.G_set = set()
        self.indies = []
        for _ in range(n_indies):
            done = False
            while not done:
                y, x = np.random.randint(0,y_max),np.random.randint(0,x_max)
                done = maze.cells[(y, x)].state == 'available'  

            self.indies.append(Indy(x, y, maze, self.available_jobs, self.indy_pos_list, self.cells, self.G, self.G_set, x_max, y_max)) 

        self.past_drawable_dicts = []
        self.past_drawable_dicts.append(self.generate_drawable_dict())

    def run(self):
        while len(self.indies) > 0:
            indies_done = []
            for i, indy in enumerate(self.indies): 
                done = indy.advance()
                if done:
                    indies_done.append(i)
            
            indies_done.reverse()
            for i in indies_done:
                del self.indies[i]

            
            self.past_drawable_dicts.append(self.generate_drawable_dict())

    def generate_drawable_dict(self):
        drawable_dict = {(cell.row, cell.col): cell.state for cell in self.cells.values()}
        for i in range(len(self.indy_pos_list)):
            pos, dir = self.indy_pos_list.pop()
            drawable_dict[tuple(pos)] = ('indy', dir)

        return drawable_dict



