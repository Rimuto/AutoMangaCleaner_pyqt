import math
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from math import sqrt, acos
from working_area_text_item import QDMTextItem

class QDMBoundingRect(QGraphicsRectItem):
    _startPos = QPointF()
    def __init__(self, item):
        super().__init__()
        self.setRect(item.boundingRect())
        self.setFlags(self.ItemIsMovable | self.ItemIsSelectable | self.ItemIsFocusable)
        self.setFiltersChildEvents(True)
        #self.setZValue(100)
        self.item = item
        self.item.setTransformOriginPoint(self.item.boundingRect().width() / 2, self.item.boundingRect().height() / 2)
        self.item.setParentItem(self)
        #self.item.setFlags(self.ItemIsSelectable)

        #self.setPen(QPen(Qt.NoPen))
        self.center = QGraphicsEllipseItem(-5, -5, 10, 10, self)
        self.center.setPen(QPen(Qt.NoPen))
        self.handle = QGraphicsRectItem(-10, -10, 20, 20, self)

        # self.vect = QGraphicsLineItem(self)
        # self.secVect = QGraphicsLineItem(self)
        # self.secVect.setPen(Qt.green)
        # self.secVect.setFlags(self.ItemIgnoresTransformations)

        self.setCenter(item.transformOriginPoint())

    def setCenter(self, center):
        self.center.setPos(center)
        self.handle.setPos(center.x(), -40)
        # self.vect.setLine(QLineF(center, self.handle.pos()))
        # self.secVect.setPos(center)
        self.setTransformOriginPoint(center)

    def updateBoundingRect(self):
        self.item.setTransformOriginPoint(self.item.boundingRect().width() / 2, self.item.boundingRect().height() / 2)
        self.setRect(self.item.boundingRect())
        self.setCenter(self.item.transformOriginPoint())

    def mouseDoubleClickEvent(self, event):
        self.item.mouseDoubleClickEvent(event)

    def sceneEventFilter(self, item, event):
        if item == self.handle:
            if (event.type() == event.GraphicsSceneMousePress
                and event.button() == Qt.LeftButton):
                    self._startPos = event.pos()
                    return True
            elif (event.type() == event.GraphicsSceneMouseMove
                and self._startPos is not None):
                    centerPos = self.center.scenePos()
                    line = QLineF(centerPos, event.scenePos())
                    self.setRotation(90 - line.angle())
                    diff = self.handle.scenePos() - centerPos
                    #self.secVect.setLine(0, 0, diff.x(), 0)
                    return True

        # if (event.type() == event.GraphicsSceneMouseDoubleClickEvent):
        #     self.item.mouseDoubleClickEvent(event)
        if (event.type() == event.GraphicsSceneMouseRelease
            and self._startPos is not None):
                self._startPos = None
                return True
        return super().sceneEventFilter(item, event)