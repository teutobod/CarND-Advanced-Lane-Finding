import numpy as np

def sliding_window_search(nonzero_pixels, img_height, start_pos_x):

    # Identify the x and y positions of all nonzero pixels in the image
    nonzeroy = np.array(nonzero_pixels[0])
    nonzerox = np.array(nonzero_pixels[1])

    # Choose number and height of sliding windows
    nwindows = 9
    window_height = np.int(img_height / nwindows)

    # Set the width of the windows +/- margin
    margin = 100
    # Set minimum number of pixels found to recenter window
    minpix = 50

    # Create empty lists to receive line pixel indices
    lane_inds = []

    # Current positions to be updated for each window
    x_current = start_pos_x
    # Step through the windows one by one
    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        win_y_low = img_height - (window + 1) * window_height
        win_y_high = img_height - window * window_height

        win_x_low = x_current - margin
        win_x_high = x_current + margin

        # Identify the nonzero pixels in x and y within the window
        good_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) &
                          (nonzerox >= win_x_low) & (nonzerox < win_x_high)).nonzero()[0]

        # Append these indices to the lists
        lane_inds.append(good_inds)

        # If you found > minpix pixels, recenter next window on their mean position
        if len(good_inds) > minpix:
            x_current = np.int(np.mean(nonzerox[good_inds]))

    # Concatenate the arrays of indices
    lane_inds = np.concatenate(lane_inds)

    # Extract ine pixel positions
    x = nonzerox[lane_inds]
    y = nonzeroy[lane_inds]
    return [x, y]

def fit_polynom(pixels: object, deg: object = 2) -> object:

    assert(len(pixels[0]) > 0)
    assert (len(pixels[1]) > 0)
    return np.polyfit(pixels[1], pixels[0], deg)

class MovingAverage:
    def __init__(self, n_window):
        self.n_window = n_window
        self.list = []

    def add(self, x):

        if(len(self.list) >= self.n_window):
            self.list.pop(0)

        self.list.append(x)

        return np.average(np.array(self.list), axis=0)

class LineFitter:

    def __init__(self):

        self.left_poly_param = None
        self.right_poly_param = None

        self.left_poly_param_av = MovingAverage(12)
        self.right_poly_param_av = MovingAverage(12)

        self.left_line_pixels = None
        self.right_line_pixels = None

        self.valid_fitting_exits = False

    def initial_fit(self, binary_img):
        img_height = binary_img.shape[0]

        # histogram of the bottom half of the image
        histogram = np.sum(binary_img[0:int(img_height / 2), :], axis=0)

        # Find left and right peaks in the histogram
        # These will be the starting points for the left and right lines
        midpoint = np.int(histogram.shape[0] / 2)
        leftx_base = np.argmax(histogram[:midpoint])
        rightx_base = np.argmax(histogram[midpoint:]) + midpoint

        nonzero = binary_img.nonzero()

        # Search for left and right pixels
        left_pixels = sliding_window_search(nonzero, img_height, leftx_base)
        right_pixels = sliding_window_search(nonzero, img_height, rightx_base)

        assert (len(left_pixels[0]) == len(left_pixels[1]))
        assert (len(right_pixels[0]) == len(right_pixels[1]))


        if len(left_pixels[0]) > 0 and len(right_pixels[0]) > 0:
            self.valid_fitting_exits = True
            self.left_line_pixels = left_pixels
            self.right_line_pixels = right_pixels

            assert (len(self.left_line_pixels[0]) > 0)
            assert (len(self.left_line_pixels[1]) > 0)

            assert (len(self.right_line_pixels[0]) > 0)
            assert (len(self.right_line_pixels[1]) > 0)
        else:
            self.__init__()

    def find_pixels_arround_line(self, binary_img, poly_param):
        nonzero = binary_img.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        margin = 100
        line_fit = poly_param
        line_inds = ((nonzerox > (line_fit[0] * (nonzeroy ** 2) + line_fit[1] * nonzeroy +
                                  line_fit[2] - margin)) & (nonzerox < (line_fit[0] * (nonzeroy ** 2) +
                                                                        line_fit[1] * nonzeroy + line_fit[
                                                                                 2] + margin)))
        line_pixels = [nonzerox[line_inds], nonzeroy[line_inds]]

        return line_pixels

    def easy_fit(self, binary_img):
        nonzero = binary_img.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        margin = 100
        left_fit = self.left_poly_param
        right_fit = self.right_poly_param

        assert(left_fit is not None)
        assert(right_fit is not None)

        left_lane_inds = ((nonzerox > (left_fit[0] * (nonzeroy ** 2) + left_fit[1] * nonzeroy +
                                       left_fit[2] - margin)) & (nonzerox < (left_fit[0] * (nonzeroy ** 2) +
                                                                             left_fit[1] * nonzeroy + left_fit[
                                                                                 2] + margin)))

        right_lane_inds = ((nonzerox > (right_fit[0] * (nonzeroy ** 2) + right_fit[1] * nonzeroy +
                                        right_fit[2] - margin)) & (nonzerox < (right_fit[0] * (nonzeroy ** 2) +
                                                                               right_fit[1] * nonzeroy + right_fit[
                                                                                   2] + margin)))

        left_pixels = [nonzerox[left_lane_inds], nonzeroy[left_lane_inds]]
        right_pixels = [nonzerox[right_lane_inds], nonzeroy[right_lane_inds]]

        assert (len(left_pixels[0]) == len(left_pixels[1]))
        assert (len(right_pixels[0]) == len(right_pixels[1]))

        if len(left_pixels[0]) > 0 and len(right_pixels[0]) > 0:
            self.valid_fitting_exits = True
            self.left_line_pixels = left_pixels
            self.right_line_pixels = right_pixels

            assert (len(self.left_line_pixels[0]) > 0)
            assert (len(self.left_line_pixels[1]) > 0)

            assert (len(self.right_line_pixels[0]) > 0)
            assert (len(self.right_line_pixels[1]) > 0)
        else:
            self.__init__()

    def fit_lines(self, binary_img):

        if self.valid_fitting_exits:
            self.easy_fit(binary_img)
        else:
            self.initial_fit(binary_img)

        if self.valid_fitting_exits:
            # Fit a second order polynomial to each

            assert (self.left_line_pixels is not None), "Left list is empty."
            assert (self.right_line_pixels is not None), "Right list is empty."

            self.left_poly_param = self.left_poly_param_av.add(fit_polynom(self.left_line_pixels))
            self.right_poly_param = self.right_poly_param_av.add(fit_polynom(self.right_line_pixels))

        return self.valid_fitting_exits

    def get_poly_params(self):
        return self.left_poly_param, self.right_poly_param
