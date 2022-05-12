# coding=utf-8
# 导入一些python包
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np
import cv2 as cv
import argparse
import imutils


# 创建一个颜色标签类
class ColorLabeler:
	def __init__(self):
		# 初始化一个颜色词典
		colors = OrderedDict({
			"red": (255, 0, 0),
			"green": (0, 255, 0),
			"blue": (0, 0, 255)})

		# 为LAB图像分配空间
		self.lab = np.zeros((len(colors), 1, 3), dtype="uint8")
		self.colorNames = []

		# 循环 遍历颜色词典
		for (i, (name, rgb)) in enumerate(colors.items()):
			# 进行参数更新
			self.lab[i] = rgb
			self.colorNames.append(name)

		# 进行颜色空间的变换
		self.lab = cv.cvtColor(self.lab, cv.COLOR_RGB2LAB)

	def label(self, image, c):
		# 根据轮廓构造一个mask，然后计算mask区域的平均值 
		mask = np.zeros(image.shape[:2], dtype="uint8")
		cv.drawContours(mask, [c], -1, 255, -1)
		mask = cv.erode(mask, None, iterations=2)
		mean = cv.mean(image, mask=mask)[:3]

		# 初始化最小距离
		minDist = (np.inf, None)

		# 遍历已知的LAB颜色值
		for (i, row) in enumerate(self.lab):
			# 计算当前l*a*b*颜色值与图像平均值之间的距离
			d = dist.euclidean(row[0], mean)

			# 如果当前的距离小于最小的距离，则进行变量更新
			if d < minDist[0]:
				minDist = (d, i)

		# 返回最小距离对应的颜色值
		return self.colorNames[minDist[1]]

# 创建形状检测类
class ShapeDetector:
	def __init__(self):
		pass

	def detect(self, c):
		# 初始化形状名和近似的轮廓
		shape = "unidentified"
		peri = cv.arcLength(c, True)
		approx = cv.approxPolyDP(c, 0.04 * peri, True)

		# 如果当前的轮廓含有3个顶点，则其为三角形
		if len(approx) == 3:
			shape = "triangle"

		# 如果当前的轮廓含有4个顶点，则其可能是矩形或者正方形
		elif len(approx) == 4:
			# 获取轮廓的边界框并计算长和宽的比例
			(x, y, w, h) = cv.boundingRect(approx)
			ar = w / float(h)

			shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

		# 如果这个轮廓含有5个顶点，则它是一个多边形
		elif len(approx) == 5:
			shape = "pentagon"

		# 否则的话，我们认为它是一个圆
		else:
			shape = "circle"

		# 返回形状的名称
		return shape


# 设置并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(ap.parse_args())

# 读取图片
image = cv.imread(args["image"])
# 进行裁剪操作
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# 进行高斯模糊操作
blurred = cv.GaussianBlur(resized, (5, 5), 0)
# 进行图片灰度化
gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
# 进行颜色空间的变换
lab = cv.cvtColor(blurred, cv.COLOR_BGR2LAB)
# 进行阈值分割
thresh = cv.threshold(gray, 60, 255, cv.THRESH_BINARY)[1]
cv.imshow("Thresh", thresh)

# 在二值图片中寻找轮廓
cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# 初始化形状检测器和颜色标签
sd = ShapeDetector()
cl = ColorLabeler()

# 遍历每一个轮廓
for c in cnts:
	# 计算每一个轮廓的中心点
	M = cv.moments(c)
	cX = int((M["m10"] / M["m00"]) * ratio)
	cY = int((M["m01"] / M["m00"]) * ratio)

	# 进行颜色检测和形状检测
	shape = sd.detect(c)
	color = cl.label(lab, c)

	# 进行坐标变换
	c = c.astype("float")
	c *= ratio
	c = c.astype("int")
	text = "{} {}".format(color, shape)
	# 绘制轮廓并显示结果
	cv.drawContours(image, [c], -1, (0, 255, 0), 2)
	cv.putText(image, text, (cX, cY), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

	cv.imshow("Image", image)
	cv.waitKey(0)

