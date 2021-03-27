import numpy as np

class Maze:
    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        
        self.maze = None
        self.generate_maze()

    def generate_maze(self):
        wall_factor = 0.3
        self.maze = {(row, col): "wall" if np.random.random() < wall_factor else "available" for row in range(self.n_rows) for col in range(self.n_cols)}

