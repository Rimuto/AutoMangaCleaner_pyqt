from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from working_area_text_item import QDMTextItem
from PyQt5.QtGui import *
import math

'''
add drawing methods to store all lines and dots
'''
class QDMWorkingAreaScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gridSize = 20
        self.gridSquares = 5
        self._color_background = QColor("#393939")
        self._light_color = QColor("#2f2f2f")
        self._dark_color = QColor("#292929")

        self._pen_light = QPen(self._light_color)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._dark_color)
        self._pen_dark.setWidth(3)

        self.textItems = []
        self.drawingItems = []


        self.empty = True
        self.mainImage = QGraphicsPixmapItem()
        self.mainImage.setTransformationMode(Qt.SmoothTransformation)

        self.dirtySpeechBubbles = []



        # self.scene_width, self.scene_height = 20000, 20000
        # self.setSceneRect(-self.scene_width//2, -self.scene_height//2, self.scene_width, self.scene_height)
        self.setBackgroundBrush(self._color_background)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def addText(self, text = "Sample Text"):
        self.textItems.append(QDMTextItem("myText"))
        self.addItem(self.textItems[-1])

    def setImage(self, pixmap=None):
        if pixmap and not pixmap.isNull():
            self.empty = False
            self.mainImage.setPixmap(pixmap)
        else:
            self.empty = True
            self.mainImage.setPixmap(QPixmap())
        self.addItem(self.mainImage)
        #self.fitInView()

    def hasPhoto(self):
        return not self.empty

    def draw(self):
        self.addEllipse(-100, -100, 0, 0, QPen(Qt.NoPen), Qt.black)

    def drawCircle(self, x, y, brushSize, pen, brush):
        self.drawingItems.append(self.addEllipse(x, y, brushSize, brushSize, pen, brush))
        print(len(self.drawingItems))

    def drawLine(self, start_x, start_y, x, y, pen):
        self.drawingItems.append(self.addLine(start_x, start_y, x, y, pen))
        print(len(self.drawingItems))

    def serialize(self):
        json = {}
        json["mainImage"] = self.mainImage
        json["dirtySpeechBubbles"] = self.dirtySpeechBubbles
        json["drawingItems"] = self.drawingItems

        return json

    # def drawBackground(self, painter, rect):
    #     super().drawBackground(painter, rect)
    #
    #     left = int(math.floor(rect.left()))
    #     right = int(math.ceil(rect.right()))
    #     top = int(math.floor(rect.top()))
    #     bottom = int(math.ceil(rect.bottom()))
    #
    #     first_left = left - (left % self.gridSize)
    #     first_top = top - (top % self.gridSize)
    #
    #     lines_light, lines_dark = [], []
    #     for x in range(first_left, right, self.gridSize):
    #         if (x % (self.gridSize * self.gridSquares)) != 0:
    #             lines_light.append(QLine(x, top, x, bottom))
    #         else:
    #             lines_dark.append(QLine(x, top, x, bottom))
    #
    #     for y in range(first_top, bottom, self.gridSize):
    #         if (y % (self.gridSize * self.gridSquares)) != 0:
    #             lines_light.append(QLine(left, y, right, y))
    #         else:
    #             lines_dark.append(QLine(left, y, right, y))
    #
    #     painter.setPen(self._pen_light)
    #     painter.drawLines(*lines_light)
    #
    #     painter.setPen(self._pen_dark)
    #     painter.drawLines(*lines_dark)

