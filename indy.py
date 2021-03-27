from drawer import Drawer
import numpy as np
from numpy import random
from maze import Maze
from cell import Cell
import networkx as nx

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
        self.path = []
        self.G = nx.Graph()
        self.G_set = set()
        self.update_graph(self.cur_pos)
        self.discover()

        self.past_drawable_dicts = []
        self.past_drawable_dicts.append(self.generate_drawable_dict())

    def take_step(self):
        pos = self.path.pop(0)
        self.update_dir(pos)
        self.cur_pos = pos

    def calc_next_goal(self):
        # Prefer to move in order: Ahead, left, right, back, Next_available_job
        theta = self.dirs_dict[self.dir]
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s), (s, c)))
        positions_to_check = R@(np.array([[1,0], [0,1], [0,-1], [-1,0]]).T)
        positions_to_check = positions_to_check.T * np.array([1,-1])
        positions_to_check = np.array(positions_to_check, dtype='int')
        positions_to_check = positions_to_check + self.cur_pos
        already_found_next_pos = False

        for pos in positions_to_check:
            try:
                # Check if the cell is available
                if self.cells[tuple(pos)].state == 'available':
                    # Check if the cell has unknown neighbours
                    neighbour_states = self.states_of_neighbours(pos)
                    if np.any(neighbour_states == 'unknown'):
                        if not already_found_next_pos:
                            already_found_next_pos = True
                            self.path.append(pos)

                        # If Indy has found a new pos but there is more available cells with unkown neighbours 
                        # those cells should be added to avaiable jobs
                        elif already_found_next_pos:
                            self.available_jobs.append(pos)

            except KeyError:
                pass

        if already_found_next_pos:
            return False
        
        # Add path to best available job
        path = self.find_next_job()
        if path is False:
            return False
        self.path.extend(path[1:])

    def update_graph(self, node):
        if tuple(node) in self.G_set:
            return
        self.G_set.add(tuple(node))

        self.G.add_node(tuple(node))
        for node_ in self.G_set:
            node_ = np.array(node_)
            if np.sum(np.abs(node-node_)) == 1:
                self.G.add_edge(tuple(node), tuple(node_))
                self.G.add_edge(tuple(node_), tuple(node))

    def find_next_job(self):
        # Start by clearing all the jobs which are already done, i.e. those cells which have already been visited
        i_to_del = []
        for i in range(len(self.available_jobs)):
            pos = self.available_jobs[i]
            neighbour_states = self.states_of_neighbours(pos)
            if np.any(neighbour_states == 'unknown'):
                continue
            i_to_del.append(i)
        
        i_to_del.reverse()
        for i in i_to_del:
            del self.available_jobs[i]
        
        if len(self.available_jobs) == 0:
            return False

        
        # Find the closest next job
        shortest_path = None
        shortest_dist = 1e10

        for goal in self.available_jobs:
            path = nx.dijkstra_path(self.G, tuple(self.cur_pos), tuple(goal))
            dist = len(path)
            if dist < shortest_dist:
                shortest_path = path

        return np.array(shortest_path)

        

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
            raise Exception("This should never happen.")
            

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

                if self.cells[tuple(pos)].state == "available":
                    self.update_graph(pos)
                
            except KeyError:
                pass
        
    def run(self):
        done = False
        while not done:
            if len(self.path) == 0:
                done = self.calc_next_goal()
                if len(self.path) == 0: break

            self.take_step()
            self.discover()
            if not done: 
                self.past_drawable_dicts.append(self.generate_drawable_dict())

    def generate_drawable_dict(self):
        drawable_dict = {(cell.row, cell.col): cell.state for cell in self.cells.values()}
        drawable_dict[tuple(self.cur_pos)] = ('indy', self.dir)
        return drawable_dict
