import numpy as np
import cv2 as cv

img_rgb = "data/1/image/1.9M.bmp"

 
R = np.eye(3)
img_size = (1280, 1024)
camera_matrix = np.array( [1433.965, 0, 639.5, 0, 1433.965, 511.5, 0, 0, 1, ]).reshape([3, 3])
distortion_coefficients = np.array( [-0.09, 0.4416, 0, -0.162]).reshape([4, 1])
mapx, mapy = cv.fisheye.initUndistortRectifyMap( camera_matrix, distortion_coefficients, R, camera_matrix, img_size, cv.CV_32FC1)
srcImg = cv.imread(img_rgb)
# srcImg = cv.imread("camera.bmp")
resultImg = cv.remap(srcImg, mapx, mapy, cv.INTER_LINEAR,  cv.BORDER_CONSTANT)
cv.imwrite("result_1.png", resultImg)
