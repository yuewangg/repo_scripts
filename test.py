import numpy as np
import cv2 as cv
from scipy.spatial import distance as dist
from collections import OrderedDict

# 创建一个颜色标签类
class ColorLabeler:
	def __init__(self):
		# 初始化一个颜色词典
		colors = OrderedDict({
			"red": (255, 0, 0),
			"green": (0, 255, 0),
            "deepblue": (30, 40, 80),
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

#定义形状检测函数
def ShapeDetection(resultImg):
    contours,hierarchy = cv.findContours(resultImg,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)  #寻找轮廓点
    for obj in contours:
        #area = cv.contourArea(obj)  #计算轮廓内区域的面积
        #cv.drawContours(imgContour, obj, -1, (255, 0, 0), 4)  #绘制轮廓线
        perimeter = cv.arcLength(obj,True)  #计算轮廓周长
        approx = cv.approxPolyDP(obj,0.02*perimeter,True)  #获取轮廓角点坐标
        CornerNum = len(approx)   #轮廓角点的数量
        x, y, w, h = cv.boundingRect(approx)  #获取坐标值和宽度、高度

        if CornerNum == 4:
            if w==h: objType= "Square"
            else:objType="Rectangle"
            cl = ColorLabeler()
            
            color = cl.label(resultImg, obj)
            if color == "deepblue":
                cv.rectangle(imgContour,(x,y),(x+w,y+h),(0,0,255),2)  #绘制边界框
                cv.putText(imgContour,objType,(x+(w//2),y+(h//2)),cv.FONT_HERSHEY_COMPLEX,0.6,(0,0,0),1)  #绘制文字
        else:objType="N"
        


img_rgb = "data/image/1.9M.bmp"

 
R = np.eye(3)
img_size = (1280, 1024)
camera_matrix = np.array( [1433.965, 0, 639.5, 0, 1433.965, 511.5, 0, 0, 1, ]).reshape([3, 3])
distortion_coefficients = np.array( [-0.09, 0.4416, 0, -0.162]).reshape([4, 1])
mapx, mapy = cv.fisheye.initUndistortRectifyMap( camera_matrix, distortion_coefficients, R, camera_matrix, img_size, cv.CV_32FC1)
srcImg = cv.imread(img_rgb)
# srcImg = cv.imread("camera.bmp")
resultImg = cv.remap(srcImg, mapx, mapy, cv.INTER_LINEAR,  cv.BORDER_CONSTANT)
cv.imwrite("result_1.png", resultImg)

imgContour = resultImg.copy()

imgGray = cv.cvtColor(resultImg,cv.COLOR_RGB2GRAY)  #转灰度图
imgBlur = cv.GaussianBlur(imgGray,(5,5),1)  #高斯模糊
#imglab = cv.cvtColor(imgBlur, cv.COLOR_BGR2LAB)
imgCanny = cv.Canny(imgBlur,60,60)  #Canny算子边缘检测
ShapeDetection(imgCanny)  #形状颜色检测

cv.imshow("Original resultImg", resultImg)
cv.imshow("imgGray", imgGray)
cv.imshow("imgBlur", imgBlur)
cv.imshow("imgCanny", imgCanny)
cv.imshow("shape Detection", imgContour)

cv.waitKey(0)

