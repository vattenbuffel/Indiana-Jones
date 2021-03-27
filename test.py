import cv2
import numpy as np


n = 10
grid = np.zeros((n,n))
grid[1, 0:5] = 1

width = 50
height = 50

img = np.zeros((n*height,n*width,3), dtype='uint8')
for row_i, row in enumerate(grid):
    for col_i, col in enumerate(row):
        color = 0
        if col == 1:
            col = 255

        img[row_i*height:row_i*height+height, col_i*width:col_i*width+width] = col

def overlay_transparent(background_img, img_to_overlay_t, x, y, overlay_size=None):
	"""
	@brief      Overlays a transparant PNG onto another image using CV2
	
	@param      background_img    The background image
	@param      img_to_overlay_t  The transparent image to overlay (has alpha channel)
	@param      x                 x location to place the top-left corner of our overlay
	@param      y                 y location to place the top-left corner of our overlay
	@param      overlay_size      The size to scale our overlay to (tuple), no scaling if None
	
	@return     Background image with overlay on top
	"""
	
	bg_img = background_img.copy()
	
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
	img1_bg = cv2.bitwise_and(roi.copy(),roi.copy(),mask = cv2.bitwise_not(mask))
	
	# Mask out the logo from the logo image.
	img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)

	# Update the original image with our new ROI
	bg_img[y:y+h, x:x+w] = cv2.add(img1_bg, img2_fg)

	return bg_img


# green = np.zeros((1000, 1000, 3), dtype='uint8')
# green[:,:] = np.array([0,255,0])


indy = cv2.imread("./img/indy.png", cv2.IMREAD_UNCHANGED)

cv2.imshow('image',overlay_transparent(img, indy, 0, 0))
cv2.waitKey(0)


indy_small = cv2.resize(indy, (width, height))
cv2.imshow("small_indy", indy_small)
cv2.waitKey(0)















