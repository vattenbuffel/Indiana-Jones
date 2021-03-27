import numpy as np
from maze import Maze
from cell import Cell

class Indy:
    def __init__(self, start_row, start_col, maze:Maze):
        self.row = start_row
        self.start_col = start_col
        self.cur_pos = np.array([start_row, start_col])
        self.maze = maze
        
        self.cells = {location: Cell(*location, "unknown") for location in maze.cells}
        self.available_jobs = []
        self.discover()

        self.past_drawable_dicts = []
        self.past_drawable_dicts.append(self.generate_drawable_dict())

    def move(self):
        # Prefer to move in order: South, West, North, East, Next_available_job
        positions_to_check = np.array([[0,1], [-1,0], [0,-1], [1,0]]) + self.cur_pos
        already_moved = False

        for pos in positions_to_check:
            try:
                # Check if the cell is available
                if self.cells[tuple(pos)].state == 'available':
                    # Check if the cell has unknown neighbours
                    neighbour_states = self.states_of_neighbours(pos)
                    if np.any(neighbour_states == 'unknown'):
                        if not already_moved:
                            # Move to that cell
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
        drawable_dict[tuple(self.cur_pos)] = 'indy'
        return drawable_dict
