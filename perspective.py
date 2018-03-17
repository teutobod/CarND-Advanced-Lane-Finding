import numpy as np
import cv2

class Transformer:
    def __init__(self):
        src = np.float32(
            [[490, 482],
             [810, 482],
             [1250, 720],
             [40, 720]])

        dst = np.float32(
            [[0, 0],
             [1280, 0],
             [1280, 720],
             [0, 720]])

        self.M = cv2.getPerspectiveTransform(src, dst)
        self.Minv = cv2.getPerspectiveTransform(dst, src)


    def to_top_view(self, img):
        img_size = (img.shape[1], img.shape[0])
        warped = cv2.warpPerspective(img, self.M, img_size, flags=cv2.INTER_LINEAR)
        return warped

    def from_top_view(self, img):
        img_size = (img.shape[1], img.shape[0])
        warped = cv2.warpPerspective(img, self.Minv, img_size, flags=cv2.INTER_LINEAR)
        return warped