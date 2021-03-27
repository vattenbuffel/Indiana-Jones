import numpy as np
from cell import Cell

class Maze:
    def __init__(self, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        
        self.cells = None
        self.generate_maze()

    def generate_maze(self):
        wall_factor = 0.3
        # wall_factor = 0
        self.cells = {(row, col): Cell(row, col, "wall" if np.random.random() < wall_factor else "available") for row in range(self.n_rows) for col in range(self.n_cols)}

    def generate_drawable_dict(self):
        return {(cell.row, cell.col): cell.state for cell in self.cells.values()}

