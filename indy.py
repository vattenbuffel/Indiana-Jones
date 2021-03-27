from drawer import Drawer
import numpy as np
from numpy import random
from maze import Maze
from cell import Cell

class Indy:
    def __init__(self, start_row, start_col, maze:Maze):
        self.row = start_row
        self.start_col = start_col
        self.cur_pos = np.array([start_row, start_col])
        self.maze = maze
        
        self.dirs_dict = {'S':3*np.pi/2, 'W':2*np.pi/2, 'N':1*np.pi/2, 'E':0}
        self.dir = np.random.choice(['S','N','W','E'])
        self.cells = {location: Cell(*location, "unknown") for location in maze.cells}
        self.available_jobs = []
        self.discover()

        self.past_drawable_dicts = []
        self.past_drawable_dicts.append(self.generate_drawable_dict())

    def move(self):
        # Prefer to move in order: Ahead, left, right, back, Next_available_job
        theta = self.dirs_dict[self.dir]
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))
        positions_to_check = R@(np.array([[1,0], [0,1], [0,-1], [-1,0]]).T)
        positions_to_check = positions_to_check.T * np.array([1,-1])
        positions_to_check = np.array(positions_to_check, dtype='int')
        positions_to_check = positions_to_check + self.cur_pos
        already_moved = False

        for pos in positions_to_check:
            try:
                # Check if the cell is available
                if self.cells[tuple(pos)].state == 'available':
                    # Check if the cell has unknown neighbours
                    neighbour_states = self.states_of_neighbours(pos)
                    if np.any(neighbour_states == 'unknown'):
                        if not already_moved:
                            # Move to that cell and update direction
                            self.update_dir(pos)
                            self.cur_pos = pos
                            already_moved = True

                        # If Indy has already moved but there is more available cells with unkown neighbours 
                        # those cells should be added to avaiable jobs
                        elif already_moved:
                            self.available_jobs.append(pos)

            except KeyError:
                pass

        if already_moved:
            return
        
        # Move to next available job
        done = False
        while not done:
            # If all of it's neighbours have already been discovered, move to next
            neighbour_states = self.states_of_neighbours(self.cur_pos)
            if np.any(neighbour_states == 'unknown'):
                return False
            else:
                if len(self.available_jobs) == 0:
                    return True
                self.cur_pos = self.available_jobs.pop()
                self.look_toward_unknown()
    
    def look_toward_unknown(self):
        pass

    def update_dir(self, next_pos):
        movement = next_pos - self.cur_pos
        if movement[0] == 1:
            self.dir = 'E'
        elif movement[0] == -1:
            self.dir = 'W'
        elif movement[1] == -1:
            self.dir = 'N'
        elif movement[1] == 1:
            self.dir = 'S'
        else:
            raise Exception("This should never happend.")
            

    def states_of_neighbours(self, cell_pos):
        positions_to_check = np.array([[0,1], [-1,0], [0,-1], [1,0]]) + cell_pos
        states = []

        for pos in positions_to_check:
            try:
                states.append(self.cells[tuple(pos)].state)
            except KeyError:
                pass
        
        return np.array(states)

    def discover(self):
        positions_to_discover = np.array([[1,0], [-1,0], [0,1], [0,-1]]) + self.cur_pos
        for pos in positions_to_discover:
            try:
                maze_state = self.maze.cells[tuple(pos)].state
                self.cells[tuple(pos)].state = maze_state
                
            except KeyError:
                pass
        
    def run(self):
        done = False
        while not done:
            done = self.move()
            self.discover()
            if not done: 
                self.past_drawable_dicts.append(self.generate_drawable_dict())

    def generate_drawable_dict(self):
        drawable_dict = {(cell.row, cell.col): cell.state for cell in self.cells.values()}
        drawable_dict[tuple(self.cur_pos)] = ('indy', self.dir)
        return drawable_dict
