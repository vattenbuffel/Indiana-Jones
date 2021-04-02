try:
    import cv2
except ModuleNotFoundError:
    print("You need to install opencv2. Try the command: pip3 install opencv-python")
    exit(0)
import numpy as np


class Drawer:
    def __init__(self, n_rows, n_cols, wall_thickness, cell_height, cell_width, cell_types=None):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.wall_thickness = wall_thickness
        self.cell_height = cell_height
        self.cell_width = cell_width
        self.cell_types = cell_types

        self.white = np.array([255,255,255])
        self.black = np.array([0,0,0])
        self.indy = cv2.imread("./img/indy.png", cv2.IMREAD_UNCHANGED)
        self.indy  = cv2.resize(self.indy, (cell_width, cell_height))
        self.indy_rotation_dict = {'N': cv2.ROTATE_180, 'S': None, 'W':cv2.ROTATE_90_CLOCKWISE , 'E':cv2.ROTATE_90_COUNTERCLOCKWISE}

        self.wall = np.zeros((cell_height, cell_width,4), dtype='uint8') 
        self.wall[:,:] = np.array((24,16,88,255))
        self.unknown = np.zeros((cell_height, cell_width,4), dtype='uint8') 
        self.unknown[:,:] = np.array((0,0,0,255))
        self.available = np.zeros((cell_height, cell_width,4), dtype='uint8') 
        self.available[:,:] = np.array((255,255,255,255))

    def draw_border(self, img):
        # Add row walls
        for row in range(self.n_rows):
            img[row*self.cell_height:row*self.cell_height+self.wall_thickness, :] = self.black
        
        for row in range(1, self.n_rows+1):
            img[row*self.cell_height-self.wall_thickness:row*self.cell_height, :] = self.black

        # Add col walls
        for col in range(self.n_cols):
            img[:, col*self.cell_width:col*self.cell_width+self.wall_thickness] = self.black
        
        for col in range(1, self.n_cols+1):
            img[:, col*self.cell_width-self.wall_thickness:col*self.cell_width] = self.black

    def draw_cell(self, img, img_to_draw, row, col, see_through=True):
        assert row >= 0 and row < self.n_rows and row % 1 == 0, f"Row must be a positive integer smaller than {self.n_rows}. It is {row}."
        assert col >= 0 and col < self.n_cols and col % 1 == 0, f"col must be a positive integer smaller than {self.n_cols}. It is {col}."
        
        if see_through:
            self.overlay_transparent(img, img_to_draw, col*self.cell_width, row*self.cell_height)
        else:
            self.fill_cell(img, img_to_draw, row*self.cell_height, col*self.cell_width)

    def fill_cell(self, img, img_to_draw, row, col):
        assert img_to_draw.shape[:2] == (self.cell_height, self.cell_width), f"Img_to_draw must have shape: {(self.cell_height, self.cell_width)}, it has: {img_to_draw.shape}."
        img[row:row+self.cell_height, col:col+self.cell_height] = img_to_draw[:,:,:3]


    @staticmethod
    def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):
        """
        @brief      Overlays a transparant PNG onto another image using CV2. Taken from https://gist.github.com/clungzta/b4bbb3e2aa0490b0cfcbc042184b0b4e.
        
        @param      background_img    The background image
        @param      img_to_overlay_t  The transparent image to overlay (has alpha channel)
        @param      x                 x location to place the top-left corner of our overlay
        @param      y                 y location to place the top-left corner of our overlay
        @param      overlay_size      The size to scale our overlay to (tuple), no scaling if None
        
        @return     Background image with overlay on top
        """
        
        # bg_img = background_img.copy()
        bg_img = background_img
        
        if overlay_size is not None:
            img_to_overlay_t = cv2.resize(img_to_overlay_t.copy(), overlay_size)

        # Extract the alpha mask of the RGBA image, convert to RGB 
        b,g,r,a = cv2.split(img_to_overlay_t)
        overlay_color = cv2.merge((b,g,r))
        
        # Apply some simple filtering to remove edge noise
        mask = cv2.medianBlur(a,5)

        h, w, _ = overlay_color.shape
        roi = bg_img[y:y+h, x:x+w]

        # Black-out the area behind the logo in our original ROI
        img1_bg = cv2.bitwise_and(roi.copy(), roi.copy(), mask = cv2.bitwise_not(mask))
        
        # Mask out the logo from the logo image.
        img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)

        # Update the original image with our new ROI
        bg_img[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)

        return bg_img

    def show_image(self, img, wait_time=0, text='Maze'):
        cv2.imshow(text, img)
        cv2.waitKey(wait_time)
        cv2.destroyAllWindows()
            
    def generate_image(self, cells):
        img = np.zeros((self.n_rows*self.cell_height, self.n_cols*self.cell_width, 3), dtype='uint8')
        img[:,:] = self.white

        for cell in cells:
            cell_type = cells[cell]
            
            if cell_type == 'wall':
                self.draw_cell(img, self.wall, *cell)
            elif cell_type == 'available':
                pass
            elif cell_type == 'unknown':
                self.draw_cell(img, self.unknown, *cell)
            elif cell_type[0] == 'indy':
                indy_img_rotated = self.indy
                if self.indy_rotation_dict[cell_type[1]] is not None:
                    indy_img_rotated = cv2.rotate(indy_img_rotated, self.indy_rotation_dict[cell_type[1]])
                self.draw_cell(img, indy_img_rotated, *cell)
            else:
                raise Exception("Should never happen.")

        self.draw_border(img)
        return img

    def generate_seq_of_imgs(self, updated_cells, img=None):
        if img is None:
            img = np.zeros((self.n_rows*self.cell_height, self.n_cols*self.cell_width, 3), dtype='uint8')
            img[:,:] = self.white
            self.draw_border(img)
        
        for cell in updated_cells:
            cell_type = updated_cells[cell]
            
            if cell_type == 'wall':
                self.draw_cell(img, self.wall, *cell, see_through=False)
            elif cell_type == 'available':
                self.draw_cell(img, self.available, *cell, see_through=False)
            elif cell_type == 'unknown':
                self.draw_cell(img, self.unknown, *cell, see_through=False)
            elif cell_type[0] == 'indy':
                indy_img_rotated = self.indy
                if self.indy_rotation_dict[cell_type[1]] is not None:
                    indy_img_rotated = cv2.rotate(indy_img_rotated, self.indy_rotation_dict[cell_type[1]])
                self.draw_cell(img, self.available, *cell, see_through=False)
                self.draw_cell(img, indy_img_rotated, *cell)
            else:
                raise Exception("Should never happen.")

        
        self.draw_border(img)
        return img


