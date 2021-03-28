import numpy as np
from cell import Cell

class Maze:
    def __init__(self, x_max, y_max):
        self.x_max = x_max
        self.y_max = y_max
        
        self.cells = None
        self.generate_maze()

    def generate_maze(self):
        # This code is based on https://gamedevelopment.tutsplus.com/tutorials/generate-random-cave-levels-using-cellular-automata--gamedev-9664
        wall_factor = 0.4 
        wall_limit = 4 
        available_limit = 5 
        n_update_steps = np.random.randint(1,10)

        cells = {(row, col): Cell(row, col, "wall" if np.random.random() < wall_factor else "available") for row in range(self.y_max) for col in range(self.x_max)}
        for i in range(n_update_steps):
            cells = self.update_alive_death(cells, wall_limit, available_limit)
        self.cells = cells

        # Make sure not all cells are walls
        good_cell_generated = False
        for cell in cells.values():
            if cell.state == 'available':
                good_cell_generated = True
                break
        if not good_cell_generated:
            self.generate_maze()


    def update_alive_death(self, cells, wall_limit, available_limit):
        new_cells = cells.copy()

        surrounding_cells = np.array([[1,0], [1,1], [0,1], [-1,1], [-1,0], [-1,-1], [0,-1], [1,-1]])
        for y in range(self.y_max):
            for x in range(self.x_max):
                # cur_cell = np.array([x, y])
                cur_cell = np.array([y, x])
                n_alive_neighbours = 0
                for surrounding_cell in surrounding_cells:
                    try:
                        n_alive_neighbours += cells[tuple(surrounding_cell + cur_cell)].state == "available"
                    except KeyError:
                        pass

                if cells[tuple(cur_cell)].state == 'available':
                    if n_alive_neighbours < wall_limit:
                        new_cells[tuple(cur_cell)].state = 'wall'

                else:
                    if n_alive_neighbours > available_limit:
                        new_cells[tuple(cur_cell)].state = 'available'
                
                
        return new_cells


    def generate_drawable_dict(self):
        return {(cell.row, cell.col): cell.state for cell in self.cells.values()}


if __name__ == '__main__':
    from drawer import Drawer

    n = 50
    drawer = Drawer(n,n,1,10,10)
    maze = Maze(n,n)
    img = drawer.generate_image(maze.generate_drawable_dict())
    drawer.show_image(img)