import matplotlib.pyplot as plt
from threshold import s_channel_threshold, l_channel_threshold
import numpy as np
import cv2

def curve_radius(poly_param, x):
    A = poly_param[0]
    B = poly_param[1]
    numerator = (1 + (2 * A * x + B) ** 2) ** 1.5
    denominator = np.absolute(2 * A)
    return numerator / denominator


def evaluate_2d_polynom_at(poly_param, x):
    A = poly_param[0]
    B = poly_param[1]
    C = poly_param[2]
    return A * x ** 2 + B * x + C

class Pipeline:

    def __init__(self, calibration, transform, line_fitter):
        self.transform = transform
        self.calibration = calibration
        self.line_fitter = line_fitter

    def process_image(self, orig_img, debug=False):
        orig_img = self.calibration.undistort(orig_img)
        img_size = {'x': orig_img.shape[1], 'y': orig_img.shape[0]}

        wraped_img = self.transform.to_top_view(orig_img)

        # Apply each of the thresholding functions
        s_binary = s_channel_threshold(wraped_img, thresh=(150, 255))
        l_binary = l_channel_threshold(wraped_img, thresh=(210, 255))

        combined_binary = np.zeros_like(s_binary)
        combined_binary[(s_binary == 1) | (l_binary == 1)] = 1

        success =  self.line_fitter.fit_lines(combined_binary)

        if not success:
            return orig_img

        left_fit, right_fit = self.line_fitter.get_poly_params()

        # Generate x and y pixel values
        ploty = np.linspace(0, img_size['y']-1, img_size['y'])
        left_fitx = evaluate_2d_polynom_at(left_fit, ploty)
        right_fitx = evaluate_2d_polynom_at(right_fit, ploty)


        ### Calculate vehicle center offset

        # Define conversions in x and y from pixels space to meters
        ym_per_pix = 30 / img_size['y']  # meters per pixel in y dimension
        xm_per_pix = 3.7 / 700  # meters per pixel in x dimension

        left_fit_bottom = evaluate_2d_polynom_at(left_fit, img_size['y'])
        right_fit_bottom = evaluate_2d_polynom_at(right_fit, img_size['y'])

        img_center_x = img_size['x'] / 2
        vehicles_center_offset_pixel = img_center_x - ((right_fit_bottom + left_fit_bottom) / 2)
        vehicles_center_offset_meter = vehicles_center_offset_pixel * xm_per_pix

        # Calculate radius
        left_fit, right_fit = self.line_fitter.get_poly_params(x=xm_per_pix, y=ym_per_pix)

        y_eval = np.max(ploty)
        left_curverad = curve_radius(left_fit, y_eval)
        right_curverad = curve_radius(right_fit, y_eval)
        curverad = (left_curverad + right_curverad) / 2

        # Draw lines on the image
        warped_zero = np.zeros_like(combined_binary).astype(np.uint8)
        color_warped = np.dstack((warped_zero, warped_zero, warped_zero))
        pts_left = np.array([np.flipud(np.transpose(np.vstack([left_fitx, ploty])))])
        pts_right = np.array([np.transpose(np.vstack([right_fitx, ploty]))])
        pts = np.hstack((pts_left, pts_right))
        cv2.polylines(color_warped, np.int_([pts]), isClosed=False, color=(255, 0, 0), thickness = 40)
        cv2.fillPoly(color_warped, np.int_([pts]), (0, 255, 0))

        new_warp = self.transform.from_top_view(color_warped)

        result = cv2.addWeighted(orig_img, 1, new_warp, 0.9, 0)

        # Print vehicle offset
        cv2.putText(result, 'Vehicle center offset : {:+.2f}m'.format(vehicles_center_offset_meter), (100, 80),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.8, color=(255, 255, 255), thickness=2)

        # Print radius of curvature on video
        cv2.putText(result, 'Lane curvature radius : {:.2f}m'.format(curverad), (120, 140),
                    fontFace=cv2.FONT_HERSHEY_DUPLEX, fontScale=1.8, color=(255, 255, 255), thickness=2)


        if debug:
            f, (axis1, axis2, axis3) = plt.subplots(1, 3, figsize=(25, 25))
            axis1.set_title('Original')
            axis1.imshow(orig_img)

            axis2.set_title('Line detection')
            axis2.imshow(wraped_img, cmap='gray')
            axis2.plot(left_fitx, ploty, color='red', linewidth=3)
            axis2.plot(right_fitx, ploty, color='red', linewidth=3)

            axis3.set_title('Result')
            axis3.imshow(result)

        return result
