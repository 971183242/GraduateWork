#from ocr.OcrWord import OcrWord
#from ocr.OcrLine import OcrLine
import random
import string

from RectangleBox.RectangleBox import RectangleBox
#from ocr.OcrProcessor import OcrProcessor
from CVProcessor.CVProcessor import CVProcessor
import cv2 as cv
import numpy as np

#CV_EVENT_LBUTTONDBLCLK





#启动

def main(path):
    print(path)#打印图片路径
    image = CVProcessor.openImage(path)#打开图片
    CVProcessor.imshow(image)
    screen_width = image.shape[1]
    screen_height = image.shape[0]
    print(screen_width,screen_height)

    gray = CVProcessor.toGray(image)  # 灰度处理
    CVProcessor.imshow(gray)
    binary = CVProcessor.getAdaptiveThreshol(gray)#二值化处理
    CVProcessor.imshow(binary)
    blur = CVProcessor.toBlur(binary)#降噪
    CVProcessor.imshow(blur)
    edge = CVProcessor.toCanny(blur)  # canny边缘检测
    CVProcessor.imshow(edge)
    dilation = CVProcessor.toDilate(edge)  # 边缘膨胀
    CVProcessor.imshow(dilation)
    blur = CVProcessor.toBlur(dilation)
    rects = CVProcessor.getContours(blur, image)  # 生成矩形boxes
    print("initial number of Boxes:",len(rects))
    #cv.imwrite("D:\\test\\save.png",image)
    RectangleBox.setBoxRelation(rects)
    print("----------------------------------------------------")
    #合并

    rects = RectangleBox.mergeBox(rects)
    print("after merge:",len(rects))


    # 打印图片信息
    '''
    for rect in rects2:
        print("w=", rect.getWidth(), "h=", rect.getHeight())
        if len(rect.getChild()) == 0:
            print("no child")
        else:
            print("child:", rect.getChild())'''


    #显示图片

    for c in rects:
        image = cv.rectangle(image, (c.getX(), c.getY()), (c.getX() + c.getWidth(), c.getY() + c.getHeight()),(0, 0, 255), 2)
        print("x=",c.getX() ,"y=",c.getY(),"w=", c.getWidth(), "h=", c.getHeight(),"parent=",c.getParent())
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        ran_str = 'D:\\Results\\'+ran_str +'.png'
        roi = image[c.getY():c.getHeight()+c.getY(),c.getX():c.getX()+c.getWidth()]
        #cv.imwrite(ran_str,roi)
    CVProcessor.imshow(image)

    print("------------------------------------------------------------------------------------------")

    def on_EVENT_LBUTTONDBLCLK(event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDBLCLK:
            xy = "%d,%d" % (x, y)
            print("x,y=",x,y)
            cv.circle(image, (x, y), 1, (255, 0, 0), thickness=-1)
            cv.putText(image, xy, (x, y), cv.FONT_HERSHEY_PLAIN,
                       1.0, (0, 0, 0), thickness=1)
            cv.imshow("image", image)
    cv.setMouseCallback('image', on_EVENT_LBUTTONDBLCLK)



if __name__ == '__main__':
    main("D:\\test\\test5.png")

