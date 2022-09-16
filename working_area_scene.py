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

        self.drawingGroup = self.createItemGroup([])
        blur = QGraphicsBlurEffect(blurRadius=1)
        self.drawingGroup.setGraphicsEffect(blur)
        self.drawingGroup.setZValue(100)

        self._color_background = QColor("#393939")

        self.textItems = []

        self.empty = True
        self.mainImage = QGraphicsPixmapItem()
        self.mainImage.setTransformationMode(Qt.SmoothTransformation)

        self.dirtySpeechBubbles = []

        self.setBackgroundBrush(self._color_background)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def addText(self, text = "Sample Text"):
        self.textItems.append(QDMTextItem("myText"))
        self.addItem(self.textItems[-1])
        self.drawingGroup.addToGroup(self.textItems[-1])

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
        item = QGraphicsEllipseItem(
            round(x), round(y),
            brushSize, brushSize,
            self.drawingGroup
        )
        item.setPen(pen)
        item.setBrush(brush)
        self.drawingGroup.addToGroup(item)

    def serialize(self):
        json = {}
        json["mainImage"] = self.mainImage
        json["dirtySpeechBubbles"] = self.dirtySpeechBubbles
        json["drawingItems"] = self.drawingItems
        return json

