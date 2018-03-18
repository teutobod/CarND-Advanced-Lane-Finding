import cv2
import numpy as np

def sobel(img, sobel_kernel, x=1, y=1):
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Take both Sobel x and y gradients
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    if x & y:
        return sobelx, sobely
    elif x:
        return sobelx
    else:
        return sobelx

def make_binary(img, thresh):
    # Create a binary image of ones where threshold is met, zeros otherwise
    binary_img = np.zeros_like(img)
    thresh_cond = (img >= thresh[0]) & (img <= thresh[1])
    binary_img[thresh_cond] = 1
    return binary_img

def scale_to_8bit(img):
    scale_factor = np.max(img) / 255
    return (img / scale_factor).astype(np.uint8)


def abs_sobel_threshold(img, orient='x', sobel_kernel=3, thresh=(0, 255)):
    if orient == 'x':
        abs_sobel = sobel(img, sobel_kernel, 1, 0)
    if orient == 'y':
        abs_sobel = sobel(img, sobel_kernel, 0, 1)

    scaled_sobel = scale_to_8bit(abs_sobel)

    return make_binary(scaled_sobel, thresh)

def magnitude_threshold(img, sobel_kernel=3, thresh=(0, 255)):
    # Apply sobel filter in x and y direction
    sobelx, sobely = sobel(img, sobel_kernel)

    # Calculate the gradient magnitude
    gradmag = np.sqrt(sobelx**2 + sobely**2)

    gradmag = scale_to_8bit(gradmag)

    return make_binary(gradmag, thresh)

def direction_threshold(img, sobel_kernel=3, thresh=(0, np.pi / 2)):
    # Apply sobel filter in x and y direction
    sobelx, sobely = sobel(img, sobel_kernel)

    # Take the absolute value of the gradient direction,
    # apply a threshold, and create a binary image result
    absgraddir = np.arctan2(np.absolute(sobely), np.absolute(sobelx))

    return make_binary(absgraddir, thresh)

def s_channel_threshold(img, thresh=(0, 255)):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    s_channel = hls[:,:,2]
    return make_binary(s_channel, thresh)

def l_channel_threshold(img, thresh=(0, 255)):
    hls = cv2.cvtColor(img, cv2.COLOR_BGR2LUV)
    l_channel = hls[:,:,0]
    return make_binary(l_channel, thresh)

def select_yellow(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    lower = np.array([20,60,60])
    upper = np.array([38,174, 250])
    mask = cv2.inRange(hsv, lower, upper)

    return mask

def select_white(image):
    lower = np.array([202,202,202])
    upper = np.array([255,255,255])
    mask = cv2.inRange(image, lower, upper)

    return mask