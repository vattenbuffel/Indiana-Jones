import multiprocessing
from networkx.algorithms.shortest_paths.generic import shortest_path

from networkx.exception import NetworkXNoPath
from drawer import Drawer
import numpy as np
from numpy import random
from maze import Maze
from cell import Cell
import networkx as nx

class Indy:
    def __init__(self, start_x, start_y, maze:Maze, available_jobs,  indy_pos_list, cells, G, G_set):
        self.y = start_y
        self.x = start_x
        self.cur_pos = np.array([start_x, start_y])
        self.maze = maze
        self.indy_pos_list = indy_pos_list
        
        self.dirs_dict = {'S':3*np.pi/2, 'W':2*np.pi/2, 'N':1*np.pi/2, 'E':0}
        self.dir = np.random.choice(['S','N','W','E'])
        self.cells = cells
        self.available_jobs = available_jobs
        self.path = []
        self.G = G
        self.G_set = G_set
        self.update_graph(self.cur_pos)
        self.discover()

        self.indy_pos_list.append((np.flip(self.cur_pos), self.dir))
        # self.past_drawable_dicts = []
        # self.past_drawable_dicts.append(self.generate_drawable_dict())

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
                if self.cells[tuple(np.flip(pos))].state == 'available':
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
        self.path = list(path[1:])

    def update_graph(self, node):
        if tuple(node) in self.G_set:
            return
        self.G_set.add(tuple(node))

        self.G.add_node(tuple(node))
        potential_neighbours = node + np.array([[1,0], [0,1], [-1,0], [0,-1]])
        for node_ in potential_neighbours:
            if tuple(node_) in self.G_set:
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
        available_jobs_set = set([tuple(job) for job in self.available_jobs])
        edges = nx.bfs_edges(self.G, tuple(self.cur_pos))
        nodes = [v for u, v in edges]
        best_goal = None
        for node in nodes:
            if node in available_jobs_set:
                best_goal = node
        
        if best_goal is None:
            return False

        # best_goal_i = nodes.index(best_goal)
        best_goal_i = [i for i in range(len(self.available_jobs)) if np.all(self.available_jobs[i]==np.array(best_goal))][0]
        shortest_path = nx.dijkstra_path(self.G, tuple(self.cur_pos), best_goal)
        assert np.all(np.abs(np.sum(np.diff(shortest_path, axis=0), axis=1)) == 1), f"The distance between all nodes in the path must be 1."


        del self.available_jobs[best_goal_i]
        return np.array(shortest_path) 

    def update_dir(self, next_pos):
        movement = next_pos - self.cur_pos
        if movement[0] == 1:
            self.dir = 'E'
            # self.dir = 'S'
        elif movement[0] == -1:
            self.dir = 'W'
            # self.dir = 'N'
        elif movement[1] == -1:
            self.dir = 'N'
            # self.dir = 'W'
        elif movement[1] == 1:
            self.dir = 'S'
            # self.dir = 'E'
        else:
            raise Exception("This should never happen.")
            
    def states_of_neighbours(self, cell_pos):
        positions_to_check = np.array([[0,1], [-1,0], [0,-1], [1,0]]) + cell_pos
        states = []

        for pos in positions_to_check:
            try:
                states.append(self.cells[tuple(np.flip(pos))].state)
            except KeyError:
                pass
        
        return np.array(states)

    def discover(self):
        positions_to_discover = np.array([[1,0], [-1,0], [0,1], [0,-1]]) + self.cur_pos
        for pos in positions_to_discover:
            try:
                maze_state = self.maze.cells[tuple(np.flip(pos))].state
                self.cells[tuple(np.flip(pos))].state = maze_state

                if self.cells[tuple(np.flip(pos))].state == "available":
                    self.update_graph(pos)
                
            except KeyError:
                pass
        
    def advance(self):
        done = False


        if len(self.path) == 0:
            done = self.calc_next_goal()
            if len(self.path) == 0: 
                done = True
        else:
            # Check if the current goal is obsolete
            state_of_goal_neighbours = self.states_of_neighbours(self.path[-1])
            if not np.any(state_of_goal_neighbours == 'unknown'):
                self.path = []
                done = self.calc_next_goal()
                if len(self.path) == 0: 
                    done = True

        if not done:
            self.take_step()
            self.discover()
            
        self.indy_pos_list.append((np.flip(self.cur_pos), self.dir))
        
        if done:
            pass

        return done

    def generate_drawable_dict(self):
        drawable_dict = {(cell.row, cell.col): cell.state for cell in self.cells.values()}
        drawable_dict[tuple(np.flip(self.cur_pos))] = ('indy', self.dir)
        return drawable_dict
