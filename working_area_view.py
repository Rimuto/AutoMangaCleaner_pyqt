from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

"""
PLAN IS:
    (DONE)  PAN & ZOOM
    (DONE)  SET IMAGE AS BACKGROUND
    (DONE)  DELETE ITEMS
    (DONE)  ADD EDITABLE TEXT ITEM
    (DONE)  BRUSH DRAWING
    LAYERS OR SMTH.? I DUNNO
    Можно рисовать на pixmap'e а не добавлять объекты на сцену, это должно помочь с лагами, если получиться 
"""

class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent = None):
        super().__init__(parent)

        self.empty = True
        self.photo = QGraphicsPixmapItem()

        #text settings
        #fonts, color, outline etc.

        #brush drawing settings
        #self.brush = QGraphicsEllipseItem
        self.drawingMode = True
        self.brushSize = 10
        self.brushColor = Qt.black
        self.lastPoint = QPoint()
        self.brush_line_pen = QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap)
        # self.brush = self.grScene.addEllipse(0, 0, self.brushSize, self.brushSize, QPen(Qt.NoPen), self.brushColor)
        #scene settings
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)

        #pan settings
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self._isPanning = False
        self._mousePressed = False

        #zoom settings
        self.zoomInFactor = 1.25
        self.zoomOutFactor = 0.8
        self.zoomClamp = False
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 20]
        if self.drawingMode:
            self.brush = self.grScene.addEllipse(0, 0, self.brushSize, self.brushSize, QPen(Qt.NoPen), self.brushColor)
            self.brush.setFlag(QGraphicsItem.ItemIsMovable)
            self.brush.setZValue(100)

    def initUI(self):
        #pass
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)


    def setMainImage(self, pixmapItem):
        self.grScene.setImage(pixmapItem)
        self.fitInView()

    def mousePressEvent(self,  event):
        if self.drawingMode and (event.button() == Qt.LeftButton):
            x = self.mapToScene(event.pos()).x()
            y = self.mapToScene(event.pos()).y()
            self.grScene.drawCircle(x - self.brushSize / 2, y - self.brushSize / 2, self.brushSize, QPen(Qt.NoPen), self.brushColor)
            self.lastPoint = self.mapToScene(event.pos())
        elif event.button() == Qt.LeftButton:
            self._mousePressed = True
            if self._isPanning:
                self.setCursor(Qt.ClosedHandCursor)
                self._dragPos = event.pos()
                event.accept()
            else:
                super(QDMGraphicsView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drawingMode:
            x = self.mapToScene(event.pos()).x()
            y = self.mapToScene(event.pos()).y()
            self.brush.setPos(x - self.brushSize / 2, y - self.brushSize / 2)
        if(event.buttons() & Qt.LeftButton) & self.drawingMode:
            x = self.mapToScene(event.pos()).x()
            y = self.mapToScene(event.pos()).y()
            #self.brush.setPos(x, y)

            self.grScene.drawLine(self.lastPoint.x(), self.lastPoint.y(), x, y, self.brush_line_pen)
            self.lastPoint = self.mapToScene(event.pos())


        elif self._mousePressed and self._isPanning:
            newPos = event.pos()
            diff = newPos - self._dragPos
            self._dragPos = newPos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())
            event.accept()
        else:
            super(QDMGraphicsView, self).mouseMoveEvent(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.modifiers() & Qt.ControlModifier:
                self.setCursor(Qt.OpenHandCursor)
            else:
                self._isPanning = False
                self.setCursor(Qt.ArrowCursor)
            self._mousePressed = False
        super(QDMGraphicsView, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control and not self._mousePressed:
            self._isPanning = True
            self.setCursor(Qt.OpenHandCursor)
        else:
            super(QDMGraphicsView, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            if not self._mousePressed:
                self._isPanning = False
                self.setCursor(Qt.ArrowCursor)
        elif event.key() == Qt.Key_Delete:
            self.deleteSelected()
        else:
            super(QDMGraphicsView, self).keyPressEvent(event)

    def deleteSelected(self):
        for item in self.grScene.selectedItems():
            self.grScene.removeItem(item)

    def getZoomStep(self, mode):
        if mode == "+":
            if self.zoom + self.zoomStep not in range(self.zoomRange[0], self.zoomRange[1]):
                return self.zoom, 1
            else:
                return self.zoom + self.zoomStep, self.zoomInFactor
        elif mode == "-":
            if self.zoom - self.zoomStep not in range(self.zoomRange[0], self.zoomRange[1]):
                return self.zoom, 1
            else:
                return self.zoom - self.zoomStep, self.zoomOutFactor
        return 10, 1

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoom, zoomFactor = self.getZoomStep("+")
        else:
            self.zoom, zoomFactor = self.getZoomStep("-")
        self.scale(zoomFactor, zoomFactor)

    # def setImage(self, pixmap=None):
    #     if pixmap and not pixmap.isNull():
    #         self.empty = False
    #         self.photo.setPixmap(pixmap)
    #     else:
    #         self.empty = True
    #         self.photo.setPixmap(QPixmap())
    #     self.fitInView()
    #
    # def hasPhoto(self):
    #     return not self.empty

    def fitInView(self, scale=True):
        rect = QRectF(self.grScene.mainImage.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.grScene.hasPhoto():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                # viewrect = self.viewport().rect()
                # scenerect = self.transform().mapRect(rect)
                # factor = min(viewrect.width() / scenerect.width(),
                #              viewrect.height() / scenerect.height())
                # self.scale(factor, factor)
            self.zoom = 5