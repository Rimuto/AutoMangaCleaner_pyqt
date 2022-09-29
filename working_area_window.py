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

    def loadImage(self):
        self.view.setMainImage(QPixmap('image.jpg'))

    def initUI(self):

        self.setGeometry(0, 0, 800, 800)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.grScene = QDMWorkingAreaScene()

        self.view = QDMGraphicsView(self.grScene, self)
        self.layout.addWidget(self.view)
        gl = QOpenGLWidget()
        gl.setMouseTracking(True)
        format = QSurfaceFormat()
        format.setSamples(4)
        gl.setFormat(format)
        self.view.setViewport(gl)
        self.setWindowTitle("AutoMangaCleaner")
        self.loadImage()
        self.show()
        #self.showMaximized()
        self.addContent()
        #self.view.setFocus()

    def mouseMoveEvent(self, event):
        self.view.mouseMoveEvent()

    def addContent(self):
        # rect = self.grScene.addRect(-50, -50, 100, 100, outlinePen, greenBrush)
        # rect.setFlag(QGraphicsItem.ItemIsSelectable)
        # rect.setFlag(QGraphicsItem.ItemIsMovable)

        # text = self.grScene.addText("SAMPLE TEXT!!!1?!!")
        # text.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        # text.setFlag(QGraphicsItem.ItemIsMovable)
        # text.setFlag(QGraphicsItem.ItemIsFocusable)
        # text.setDefaultTextColor(QColor.fromRgbF(1.0, 1.0, 1.0))

        #tagItem = QDMTextItem("myText")  # create a NodeTag item
        self.grScene.addText()
