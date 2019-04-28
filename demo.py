#from ocr.OcrWord import OcrWord
#from ocr.OcrLine import OcrLine
from RectangleBox.RectangleBox import RectangleBox
#from ocr.OcrProcessor import OcrProcessor
from CVProcessor.CVProcessor import CVProcessor
import cv2 as cv
#from rule.OcrRule import OcrRule
#from rule.MergeRule import MergeRule
#from ocr.MergedWord import MergedWord
#from structure.StructureBuilder import StructureBuilder
#from code.CodeProcessor import CodeProcessor
from DecisionTree import DecisionTree


#启动

def main(path):
    print(path)#打印图片路径
    image = CVProcessor.openImage(path)#打开图片
    #CVProcessor.imshow(image)
    screen_width = image.shape[1]
    screen_height = image.shape[0]
    print(screen_width,screen_height)

    gray = CVProcessor.toGray(image)  # 灰度处理
    binary = CVProcessor.getAdaptiveThreshol(gray)#二值化处理
    blur = CVProcessor.toBlur(binary)#降噪
    edge = CVProcessor.toCanny(blur)  # canny边缘检测
    dilation = CVProcessor.toDilate(edge)  # 边缘膨胀
    rects = CVProcessor.getContours(dilation, image)  # 生成矩形boxes
    print("initial number of Boxes:",len(rects))
    #cv.imwrite("D:\\test\\save.png",image)
    RectangleBox.setBoxRelation(rects)
    print("----------------------------------------------------")
    #合并
    rects2 = RectangleBox.mergeBox(rects)
    print("after merge:",len(rects2))
    rects3 = RectangleBox.mergeBox(rects2)
    print("after merge:", len(rects3))
    # 打印图片信息
    '''
    for rect in rects2:
        print("w=", rect.getWidth(), "h=", rect.getHeight())
        if len(rect.getChild()) == 0:
            print("no child")
        else:
            print("child:", rect.getChild())'''


    #显示图片
    for c in rects2:
        image = cv.rectangle(image, (c.getX(), c.getY()), (c.getX() + c.getWidth(), c.getY() + c.getHeight()),(0, 0, 255), 2)
        print("y=",c.getY(),"w=", c.getWidth(), "h=", c.getHeight())
    CVProcessor.imshow(image)





if __name__ == '__main__':
    main("D:\\test\\test3.png")