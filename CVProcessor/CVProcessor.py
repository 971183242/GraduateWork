import cv2 as cv
import math
import numpy as np
from matplotlib import pyplot as plt
from RectangleBox.RectangleBox import RectangleBox
class CVProcessor:

    #加载图片
    def openImage(path):
        img = cv.imread(path,cv.IMREAD_COLOR)
        #cv.namedWindow('demo',cv.WINDOW_AUTOSIZE)
        #CVProcessor.imshow(img)

        return img


    #显示图片
    def imshow(img):
        cv.namedWindow("image",0)
        cv.imshow("image",img)
        cv.waitKey()
        cv.destroyAllWindows()



    #灰度处理
    def toGray(img):
        gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
        #CVProcessor.imshow(gray)
        return gray


    #二值化处理
    def getAdaptiveThreshol(gray):
        binary = cv.adaptiveThreshold(gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,25,5)
        #CVProcessor.imshow(binary)
        return binary

    #滤波
    def toBlur(img):
        blurResult = cv.medianBlur(img,5)#中值滤波
        blurResult = cv.boxFilter(blurResult,-1,(5,5))

        blurResult = cv.GaussianBlur(blurResult,(5,5),0)#高斯滤波

        #CVProcessor.imshow(blurResult)
        return blurResult


    #边缘检测
    def toCanny(binary):
        edge = cv.Canny(binary,30,150)
        #CVProcessor.imshow(edge)
        return edge

    #边缘膨胀
    def toDilate(edge):
        kernel = cv.getStructuringElement(cv.MORPH_RECT,(3,3))
        dilated = cv.dilate(edge,kernel)
        #CVProcessor.imshow(dilated)
        return dilated




    #画矩形
    def getContours(blur,image):
        results = []
        contours, hierarchy = cv.findContours(blur, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        #print(len(contours))
        for c in contours:
            x,y,w,h = cv.boundingRect(c)
            res = RectangleBox(x,y,w,h)
            results.append(res)

        #霍夫识别圆形
        sin = math.sin(math.pi * 45 / 180)
        circles = cv.HoughCircles(blur, cv.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=10, maxRadius=100)
        for c in circles[0, :]:
            x = int(c[0] - sin * c[2])
            y = int(c[1] - sin * c[2])
            w = int(2 * c[2] * sin)
            h = int(2 * c[2] * sin)
            res = RectangleBox(x, y, w, h)
            results.append(res)
            #cv.circle(image,(c[0],c[1]),c[2],(255,0,0),2)

        #CVProcessor.imshow(image)
        return results





if __name__ == '__main__':
    img = CVProcessor.openImage("D:\\test\\test3.png")
    screen_width = img.shape[1]
    screen_height = img.shape[0]
    print(screen_width, screen_height)
    gray = CVProcessor.toGray(img)
    binary = CVProcessor.getAdaptiveThreshol(gray)
    edge = CVProcessor.toCanny(binary)
    dilation = CVProcessor.toDilate(edge)
    blur = CVProcessor.toBlur(dilation)
    rects = CVProcessor.getContours(blur,img)
    RectangleBox.setBoxRelation(rects)
    image = img

    rects = RectangleBox.mergeBox(rects)
    for c in rects:
        image = cv.rectangle(image, (c.getX(), c.getY()), (c.getX() + c.getWidth(), c.getY() + c.getHeight()), (0, 0, 255), 2)
    CVProcessor.imshow(image)





