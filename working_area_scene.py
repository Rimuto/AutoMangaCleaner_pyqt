from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from working_area_text_item import QDMTextItem
from PyQt5.QtGui import *
from working_area_bounding_rect import QDMBoundingRect
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

        self.imageItems = {}
        self.textItems = []

        self.empty = True
        self.mainImage = QGraphicsPixmapItem()
        self.mainImage.setTransformationMode(Qt.SmoothTransformation)
        self.mainImage.setZValue(0)

        self.dirtySpeechBubbles = []

        self.setBackgroundBrush(self._color_background)

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def addText(self, text = "Sample Text"):
        self.textItems.append(QDMBoundingRect(QDMTextItem("myText")))
        self.addItem(self.textItems[-1])
        self.textItems[-1].setZValue(100)
        # self.drawingGroup.addToGroup(self.textItems[-1])

    def addIntaractiveImage(self, image):
        image = QDMBoundingRect(image)
        rect = image.rect()
        rect.setWidth(10)
        rect.setHeight(10)
        image.setMinimalRect(rect)
        self.addItem(image)

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

    def addImage(self, x, y, image, tag):
        self.imageItems[tag] = self.addPixmap(QPixmap(image))
        self.imageItems[tag].setPos(x, y)

    def delImage(self, tag):
        self.removeItem(self.imageItems[tag])

    def serialize(self):
        json = {}
        json["mainImage"] = self.mainImage
        json["dirtySpeechBubbles"] = self.dirtySpeechBubbles
        json["drawingItems"] = self.drawingItems
        return json

