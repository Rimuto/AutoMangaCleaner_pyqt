import math
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from math import sqrt, acos
from working_area_text_item import QDMTextItem

class QDMBoundingRect(QGraphicsRectItem):
    _startPos = QPointF()
    handleMiddleRight = 5
    handleBottomMiddle = 7
    handleBottomRight = 8

    handleSize = +10.0
    handleSpace = -4.0

    handleCursors = {
        handleMiddleRight: Qt.SizeHorCursor,
        handleBottomMiddle: Qt.SizeVerCursor,
        handleBottomRight: Qt.SizeFDiagCursor,
    }

    def __init__(self, item):
        super().__init__()
        self.borderColor = Qt.blue
        self.backgroundColor = Qt.white

        self.pen = QPen(self.borderColor)
        self.brush = QBrush(self.backgroundColor)

        self.setRect(item.boundingRect())
        self.minimalRect = item.boundingRect()
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
        self.handle.setPen(self.pen)
        self.handle.setBrush(self.brush)

        # self.vect = QGraphicsLineItem(self)
        # self.secVect = QGraphicsLineItem(self)
        # self.secVect.setPen(Qt.green)
        # self.secVect.setFlags(self.ItemIgnoresTransformations)

        self.setCenter(item.transformOriginPoint())

        self.hide_handles = True
        self.handles = {}
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.updateHandlesPos()
        self.hideRect()

    def setMinimalRect(self, rect):
        self.minimalRect = rect

    def handleAt(self, point):
        """
        Returns the resize handle below the given point.
        """
        print(point)
        for k, v, in self.handles.items():
            if v.contains(point):
                return k
        return None

    def hoverMoveEvent(self, moveEvent):
        """
        Executed when the mouse moves over the shape (NOT PRESSED).
        """
        if self.isSelected():
            handle = self.handleAt(moveEvent.pos())
            cursor = Qt.ArrowCursor if handle is None else self.handleCursors[handle]
            self.setCursor(cursor)
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        """
        Executed when the mouse leaves the shape (NOT PRESSED).
        """
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)

    def hideHandles(self):
        self.handles[self.handleMiddleRight].setVisible(False)
        self.handles[self.handleBottomMiddle].setVisible(False)
        self.handles[self.handleBottomRight].setVisible(False)

    def hideRect(self):
        self.setPen(QPen(Qt.NoPen))
        self.handle.setVisible(False)
        self.hide_handles = True

    def showRect(self):
        self.setPen(QPen(Qt.blue))
        self.handle.setVisible(True)
        self.hide_handles = False

    def paint(self, painter, option, widget=None):
        option.state &= ~QStyle.State_Selected
        super().paint(painter, option, widget)
        if self.isSelected():
            self.showRect()
        elif not self.isSelected():
            self.hideRect()

        # if isinstance(self.item, QGraphicsPixmapItem):
        #     painter.drawPixmap(self.x(), self.y(), self.rect().width(), self.rect().height(),
        #                   self.item.pixmap().scaled(self.rect().width(), self.rect().height(), transformMode=QtCore.Qt.SmoothTransformation))

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)#self.brush
        painter.setPen(Qt.NoPen)#self.pen
        for handle, rect in self.handles.items():
            if self.handleSelected is None or handle == self.handleSelected:
                if self.hide_handles == False:
                    painter.drawRect(rect)

    def setCenter(self, center):
        self.center.setPos(center)
        self.handle.setPos(center.x(), -40)
        # self.vect.setLine(QLineF(center, self.handle.pos()))
        # self.secVect.setPos(center)
        self.setTransformOriginPoint(center)

    def updateBoundingRect(self):
        if isinstance(self.item, QDMTextItem):
            self.item.setTextWidth(self.rect().width())

        self.item.setTransformOriginPoint(self.item.boundingRect().width() / 2, self.item.boundingRect().height() / 2)
        #if self.item.boundingRect().height() > self.rect().height():
        self.setRect(self.item.boundingRect())
        self.setCenter(self.rect().center())
        self.updateHandlesPos()

    def mouseDoubleClickEvent(self, event):
        self.item.mouseDoubleClickEvent(event)

    def sceneEventFilter(self, item, event):
        if item == self.handle:
            if event.type() == event.GraphicsSceneMousePress and event.button() == Qt.LeftButton:
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

    def mousePressEvent(self, mouseEvent):
        """
        Executed when the mouse is pressed on the item.
        """
        self.handleSelected = self.handleAt(mouseEvent.pos())
        if self.handleSelected:
            self.mousePressPos = mouseEvent.pos()
            self.mousePressRect = self.boundingRect()
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        """
        Executed when the mouse is being moved over the item while being pressed.
        """
        if self.handleSelected is not None:
            self.interactiveResize(mouseEvent.pos())
        else:
            super().mouseMoveEvent(mouseEvent)

    def mouseReleaseEvent(self, mouseEvent):
        """
        Executed when the mouse is released from the item.
        """
        super().mouseReleaseEvent(mouseEvent)
        self.handleSelected = None
        self.mousePressPos = None
        self.mousePressRect = None
        self.update()

    def boundingRect(self):
        """
        Returns the bounding rect of the shape (including the resize handles).
        """
        o = self.handleSize + self.handleSpace
        return self.rect().adjusted(-o, -o, o, o)

    def updateHandlesPos(self):
        """
        Update current resize handles according to the shape size and position.
        """
        s = self.handleSize
        b = self.boundingRect()
        #self.handles[self.handleTopLeft] = QRectF(b.left(), b.top(), s, s)
        #self.handles[self.handleTopMiddle] = QRectF(b.center().x() - s / 2, b.top(), s, s)
        #self.handles[self.handleTopRight] = QRectF(b.right() - s, b.top(), s, s)
        #self.handles[self.handleMiddleLeft] = QRectF(b.left(), b.center().y() - s / 2, s, s)
        self.handles[self.handleMiddleRight] = QRectF(b.right() - s, b.top() + s, s, self.rect().height() - s)
        #self.handles[self.handleBottomLeft] = QRectF(b.left(), b.bottom() - s, s, s)
        self.handles[self.handleBottomMiddle] = QRectF(b.left() + s, b.bottom() - s, self.rect().width() - s, s)
        self.handles[self.handleBottomRight] = QRectF(b.right() - s, b.bottom() - s, s, s)

    def interactiveResize(self, mousePos):
        """
        Perform shape interactive resize.
        """
        offset = self.handleSize + self.handleSpace
        boundingRect = self.boundingRect()
        rect = self.rect()
        diff = QPointF(0, 0)

        self.prepareGeometryChange()

        if self.handleSelected == self.handleMiddleRight:
            print("MR")
            fromX = self.mousePressRect.right()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            diff.setX(toX - fromX)
            boundingRect.setRight(toX)
            if boundingRect.width() > self.minimalRect.width():
                rect.setRight(boundingRect.right() - offset)
                self.setRect(rect)

        if self.handleSelected == self.handleBottomMiddle:

            fromY = self.mousePressRect.bottom()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setY(toY - fromY)
            boundingRect.setBottom(toY)
            rect.setBottom(boundingRect.bottom() - offset)
            self.setRect(rect)

        if self.handleSelected == self.handleBottomRight:

            fromX = self.mousePressRect.right()
            fromY = self.mousePressRect.bottom()
            toX = fromX + mousePos.x() - self.mousePressPos.x()
            toY = fromY + mousePos.y() - self.mousePressPos.y()
            diff.setX(toX - fromX)
            diff.setY(toY - fromY)
            boundingRect.setRight(toX)
            boundingRect.setBottom(toY)
            if boundingRect.width() > self.minimalRect.width():
                rect.setRight(boundingRect.right() - offset)
                rect.setBottom(boundingRect.bottom() - offset)
                self.setRect(rect)
            if boundingRect.width() < self.minimalRect.width() and boundingRect.height() > self.minimalRect.height():
                rect.setBottom(boundingRect.bottom() - offset)
                self.setRect(rect)
            if boundingRect.width() > self.minimalRect.width() and boundingRect.height() < self.minimalRect.height():
                rect.setRight(boundingRect.right() - offset)
                self.setRect(rect)
        self.updateBoundingRect()
        self.updateHandlesPos()

    def shape(self):
        """
        Returns the shape of this item as a QPainterPath in local coordinates.
        """
        path = QPainterPath()
        path.addRect(self.rect())
        if self.isSelected():
            for shape in self.handles.values():
                path.addEllipse(shape)
        return path
