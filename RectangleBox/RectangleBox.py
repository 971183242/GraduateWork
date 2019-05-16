#cv边缘框

class RectangleBox:

    def __init__(self, x,y,w,h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h

        self.parent = -1#直接父框的下标
        self.childs = []#包含的直接子框的下标

        self.isAsDividingLine = False#作为first划分的line
        self.isAsFirstStructure = False#是否是structure的第一层

        self.isBeMerged = False#是否被合并


    def getX(self):
        return self.x

    def setX(self,x):
        self.x = x

    def getY(self):
        return self.y

    def setY(self,y):
        self.y = y

    def getPoint(self):
        return (self.x,self.y)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setHeight(self,h):
        self.height = h

    def setWidth(self,w):
        self.width = w

    def getParent(self):
        return self.parent

    def getChild(self):
        return self.childs

    def setChild(self,child_list):
        self.childs = child_list

    def setParent(self,parent):
        self.parent = parent

    def addChild(self,child):
        self.childs.append(child)

    def setIsAsDividingLine(self,isDividingLine):
        self.isAsDividingLine = isDividingLine

    def getIsAsDividingLine(self):
        return self.isAsDividingLine

    def setIsAsFirstStructure(self,isFirst):
        self.isAsFirstStructure = isFirst

    def getIsAsFirstStructure(self):
        return self.isAsFirstStructure

    def getIsBeMerged(self):
        return self.isBeMerged

    def setIsBeMerged(self,isBeMerged):
        self.isBeMerged = isBeMerged

    # 判断是否有交
    def isOverlap(self, rect):
        x, y = rect.getPoint()
        w = rect.getWidth()
        h = rect.getHeight()
        if not ((self.x+self.width < x or self.y+self.height<y) or \
            (x+w<self.x or y+h<self.y)) :
            return True
        else:
            return False


    #是否包含了另一个box
    def isContain(self,another):
        if self.x <= another.x and self.y <=another.y and \
            self.x + self.width >= another.x + another.width and \
            self.y + self.height >= another.y + another.height :
            return True
        else:
            return False

    #是否被包含
    #self contain another
    def isBeContained(self,another):
        if (self.x >= another.x and self.y >= another.y and \
                self.x + self.width <= another.x + another.width and \
                self.y + self.height <= another.y + another.height) :
            return True
        else:
            return False

    #建立树关系
    @staticmethod
    def setBoxRelation(rects):
        i = 0
        while i < len(rects):
            j = 0
            while j < len(rects):
                if i == j:#不与自己进行比较
                    j = j + 1
                    continue
                if rects[i].isBeContained(rects[j]):
                    parent_temp = rects[i].getParent()
                    if parent_temp == -1:
                        rects[i].setParent(j)
                    elif rects[j].isBeContained(rects[parent_temp]):
                        rects[i].setParent(j)
                j = j + 1
            i = i + 1

        for rect in rects:
            parent = rect.getParent()
            if parent != -1:
                rects[parent].addChild(rects.index(rect))#index方法返回查找对象的索引位置，如果没有找到对象则抛出异常。


    def isNearBy(self, rect):
        x, y = rect.getPoint()
        w = rect.getWidth()
        h = rect.getHeight()
        if ((self.y -3 < y < self.y + 3) or(y-3<self.y<y+3 ))and (self.x + self.width - x < 50 ):
            return True
        else:
            return False

    @staticmethod
    def mergeBox(rects):

        result = []
        for rect in rects:
            if rect.getParent() == -1 and rect.getWidth() > 140 and rect.getWidth() < 1000:
                result.append(rect)
        rects = result

        # 合并矩形

        i = 0;
        while i < len(rects):
            j = i + 1
            while j < len(rects):
                if i < len(rects) and rects[i].height < 100 and rects[i].isNearBy(rects[j]):
                    temp = RectangleBox(min(rects[i].x, rects[j].x), min(rects[i].y, rects[j].y),
                                        max(rects[i].x + rects[i].width,
                                            rects[j].x + rects[j].width - min(rects[i].x, rects[j].x)),
                                        max(rects[i].y + rects[i].height, rects[j].y + rects[j].height) - min(
                                            rects[i].y, rects[j].y))
                    rects[i] = temp
                    rects.remove(rects[j])

                j = j + 1
            i = i + 1

        i = 0;
        while i < len(rects):
            j = i + 1
            while j < len(rects):
                if i < len(rects) and rects[i].height < 100 and rects[i].isOverlap(rects[j]):
                    temp = RectangleBox(min(rects[i].x, rects[j].x), min(rects[i].y, rects[j].y),
                                        max(rects[i].x + rects[i].width,
                                            rects[j].x + rects[j].width - min(rects[i].x, rects[j].x)),
                                        max(rects[i].y + rects[i].height, rects[j].y + rects[j].height) - min(
                                            rects[i].y, rects[j].y))
                    rects[i] = temp
                    rects.remove(rects[j])

                j = j + 1
            i = i + 1


        result = []
        for rect in rects:
            if rect.getParent() == -1 and (rect.getHeight()> 60 or rect.getWidth()>100) and rect.getWidth()<1000:
                result.append(rect)
        rects = result

        """
         i = 0;
        while i < len(rects):
            j = i + 1
            while j < len(rects):
                if i < len(rects) and rects[i].isNearBy(rects[j]):
                    temp = RectangleBox(min(rects[i].x, rects[j].x), min(rects[i].y, rects[j].y),
                                        max(rects[i].x + rects[i].width, rects[j].x + rects[j].width),
                                        max(rects[i].y + rects[i].height, rects[j].y + rects[j].height))
                    rects[i] == temp
                    rects.remove(rects[j])

                j = j + 1
            i = i + 1
        """


        return rects
"""

"""





