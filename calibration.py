import numpy as np
import cv2
import glob
import pickle

class Calibration:

    def do_calibration(self, calibration_path, nx, ny):
        objp = np.zeros((ny * nx, 3), np.float32)
        objp[:, :2] = np.mgrid[0:nx, 0:ny].T.reshape(-1, 2)

        # Arrays to store object points and image points from all the images.
        objpoints = []  # 3d points in real world space
        imgpoints = []  # 2d points in image plane.

        # Make a list of calibration images
        images = glob.glob(calibration_path + '/*.jpg')

        for idx, fname in enumerate(images):
            img = cv2.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)

            if ret == True:
                objpoints.append(objp)
                imgpoints.append(corners)
                cv2.drawChessboardCorners(img, (nx, ny), corners, ret)

        img = cv2.imread(images[0])
        img_size = (img.shape[1], img.shape[0])
        # Do camera calibration given object points and image points
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_size, None, None)

        self.calibration_data = (mtx, dist)

        return ret

    def calibrate(self, calibration_path, nx=9, ny=6):
        cal_datat_file = calibration_path + "/calibration_data.p"
        try:
            with open(cal_datat_file, "rb") as f:
                self.calibration_data = pickle.load(f)
        except Exception as error:
            if self.do_calibration(calibration_path, nx, ny):
                pickle.dump(self.calibration_data, open(cal_datat_file, "wb"))

    def undistort(self, img):
        mtx = self.calibration_data[0]
        dist = self.calibration_data[1]
        return cv2.undistort(img, mtx, dist, None, mtx)