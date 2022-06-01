# coding=utf-8
from calendar import c
from importlib.resources import path
from cv2 import displayStatusBar
import numpy as np
import cv2 as cv
from pyrsistent import b
from scipy.spatial import distance as dist
import os

KNOWN_WIDTH = 117.3/2.54
KNOWN_HEIGHT = 165.2/2.54
FOCALLENGTH = 1433.965

# 注意，英寸与cm之间的单位换算为： 1英寸=2.54cm

def distance_to_camera(knownWidth, focalLength, perWidth):
    return (knownWidth * focalLength) / perWidth

distance = []
R = np.eye(3)
img_size = (1280, 1024)
camera_matrix = np.array( [1433.965, 0, 639.5, 0, 1433.965, 511.5, 0, 0, 1, ]).reshape([3, 3])
distortion_coefficients = np.array( [-0.09, 0.4416, 0, -0.162]).reshape([4, 1])
mapx, mapy = cv.fisheye.initUndistortRectifyMap( camera_matrix, distortion_coefficients, R, camera_matrix, img_size, cv.CV_32FC1)

path = "data/image/"
img_list = os.listdir(path)
print("输入图像：",img_list)
for img in img_list:

	minDist = 99999999999
	srcImg = cv.imread(path + img)

	resultImg = cv.remap(srcImg, mapx, mapy, cv.INTER_LINEAR,  cv.BORDER_CONSTANT)

	imgContour = resultImg.copy()

	imgGray = cv.cvtColor(resultImg,cv.COLOR_BGR2GRAY)  #转灰度图
	imgBlur = cv.GaussianBlur(imgGray,(5,5),1)  #高斯模糊
	#imglab = cv.cvtColor(imgBlur, cv.COLOR_BGR2LAB)
	imgCanny = cv.Canny(imgBlur,60,60)  #Canny算子边缘检测

	contours,hierarchy = cv.findContours(imgCanny,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)  #寻找轮廓点
	for obj in contours:
		#area = cv.contourArea(obj)  #计算轮廓内区域的面积
		#cv.drawContours(imgContour, obj, -1, (255, 0, 0), 4)  #绘制轮廓线
		perimeter = cv.arcLength(obj,True)  #计算轮廓周长
		approx = cv.approxPolyDP(obj,0.02*perimeter,True)  #获取轮廓角点坐标
		CornerNum = len(approx)   #轮廓角点的数量
		x, y, w, h = cv.boundingRect(approx)  #获取坐标值和宽度、高度

		if CornerNum == 4 and w!=h:
			rect = cv.minAreaRect(obj)
			bgr = resultImg[int(rect[0][1])][int(rect[0][0])]
				# 计算当前l*a*b*颜色值与图像平均值之间的距离
			d = dist.euclidean((80,45,30), bgr)
				# 如果当前的距离小于最小的距离，则进行变量更新
			if d < minDist:
				newobj = obj
				minDist = d

	rect = cv.minAreaRect(newobj)
	area = cv.contourArea(newobj)
	dis_S = pow((KNOWN_HEIGHT * KNOWN_WIDTH / area) * (FOCALLENGTH ** 2), 0.5)
	dis_w = distance_to_camera(KNOWN_WIDTH, FOCALLENGTH, rect[1][0])
	dis_h = distance_to_camera(KNOWN_HEIGHT, FOCALLENGTH, rect[1][1])
	dis = (dis_w + dis_h + dis_S)*2.54/3000
	distance.append(dis)
print("预测值：",distance)
a = round((distance[0]-1.9)*100/1.9,2)
b = round((distance[1]-2.5)*100/2.5,2)
c = round((distance[2]-3.1)*100/3.1,2)
print("误差值： [",a,"% ，",b,"% ，",c,"% ]")
print(area)


