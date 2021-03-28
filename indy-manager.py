from cell import Cell
from maze import Maze
from indy import Indy
import numpy as np

class IndyManager:
    def __init__(self, n_row, n_col, maze:Maze, n_workers = 1):
        self.n_workers = n_workers
        self.maze = maze
        self.available_jobs = []
        self.indy_pos_list = []
        self.cells = {location: Cell(*location, "unknown") for location in maze.cells}

        indies = [Indy(np.random.randint(0,n_row),np.random.randint(0,n_col), maze, self.available_jobs, self.indy_pos_list, self.cells)]

        self.past_drawable_dicts = []
        self.past_drawable_dicts.append(self.generate_drawable_dict())

    def run(self):
        while len(self.indies) > 0:
            indies_done = []
            for i, indy in enumerate(self.indies): 
                done = indy.advance()
                if done:
                    indies_done.append(i)
            
            del self.indies[i]

            
            self.past_drawable_dicts.append(self.generate_drawable_dict())

        

    def generate_drawable_dict(self):
        drawable_dict = {(cell.row, cell.col): cell.state for cell in self.cells.values()}
        for i in range(self.n_workers):
            pos, dir = self.indy_pos_list.pop()
            drawable_dict[tuple(pos)] = ('indy', dir)

        return drawable_dict



