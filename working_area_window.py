import sys
from PyQt5.QtWidgets import *
from working_area_scene import QDMWorkingAreaScene
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from working_area_view import QDMGraphicsView
from working_area_text_item import QDMTextItem


class WorkingArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def getScene(self):
        return self.view.grScene

    def setScene(self, scene):
        self.view.grScene = scene
        self.view.setScene(self.view.grScene)
        self.view.fitInView()
        self.view.initBrushCursor()

    def loadImage(self, path="image.jpg"):
        self.view.setMainImage(QPixmap(path))

    def initUI(self):
        self.setGeometry(0, 0, 800, 800)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        #self.grScene = QDMWorkingAreaScene()
        self.view = QDMGraphicsView(self)


        self.layout.addWidget(self.view)
        gl = QOpenGLWidget()
        gl.setMouseTracking(True)
        format = QSurfaceFormat()
        format.setSamples(4)
        gl.setFormat(format)
        self.view.setViewport(gl)
        #self.setWindowTitle("AutoMangaCleaner")
        self.loadImage()
        self.show()
        #self.showMaximized()
        self.addText()
        #self.view.setFocus()

    def mouseMoveEvent(self, event):
        self.view.mouseMoveEvent()

    def setLineHeight(self, value):
        self.view.setLineHeight(value)

    def addImage(self, x, y, image, tag):
        self.view.addImage(x, y, image, tag)

    def delImage(self, tag):
        self.view.delImage(tag)

    def setTextFont(self, font):
        self.view.setTextItemFont(font)

    def setTextFontSize(self, value):
        self.view.setFontSize(value)

    def setRotationAngle(self, value):
        self.view.setRotationAngle(value)

    def deleteSelectedObject(self):
        self.view.deleteSelected()

    def addText(self):
        # rect = self.grScene.addRect(-50, -50, 100, 100, outlinePen, greenBrush)
        # rect.setFlag(QGraphicsItem.ItemIsSelectable)
        # rect.setFlag(QGraphicsItem.ItemIsMovable)

        # text = self.grScene.addText("SAMPLE TEXT!!!1?!!")
        # text.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        # text.setFlag(QGraphicsItem.ItemIsMovable)
        # text.setFlag(QGraphicsItem.ItemIsFocusable)
        # text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        #tagItem = QDMTextItem("myText")  # create a NodeTag item
        self.view.addText()
