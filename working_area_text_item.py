from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class QDMTextItem(QGraphicsTextItem):
    def __init__(self, text):
        QGraphicsTextItem.__init__(self, text)
        self.startPos = None
        self.isMoving = False
        #self.setFlag(QGraphicsTextItem.ItemIsSelectable)
        #self.setFlag(QGraphicsTextItem.ItemIsMovable)
        #self.setZValue(1)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        # the following is useless, not only because we are leaving the text
        # painting to the base implementation, but also because the text is
        # already accessible using toPlainText() or toHtml()
        # self.text = text
        # this is unnecessary too as all new items always have a (0, 0) position
        # self.setPos(0, 0)

    def boundingRect(self):
        return super().boundingRect() | QRectF(0, 0, 80, 25)

    def paint(self, painter, option, widget):
        #painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
        #painter.drawRect(self.boundingRect())
        super().paint(painter, option, widget)

    def shape(self):
        shape = QPainterPath()
        shape.addRect(self.boundingRect())
        return shape

    def focusOutEvent(self, event):
        self.setTextInteractionFlags(Qt.NoTextInteraction)

    def mouseDoubleClickEvent(self, event):
        if (not self.isMoving and
                self.textInteractionFlags() != Qt.TextEditorInteraction):
            self.setTextInteractionFlags(Qt.TextEditorInteraction)
            self.setFocus()
            textCursor = self.textCursor()
            self.setTextCursor(textCursor)


    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.parentItem().updateBoundingRect()

    # def mousePressEvent(self, event):
    #     if (event.button() == Qt.LeftButton and
    #             self.textInteractionFlags() != Qt.TextEditorInteraction):
    #         self.startPos = event.pos()
    #     else:
    #         super().mousePressEvent(event)

    # def mouseMoveEvent(self, event):
    #     if self.startPos:
    #         delta = event.pos() - self.startPos
    #         if (self.isMoving or
    #                 delta.manhattanLength() >= QApplication.startDragDistance()):
    #             self.setPos(self.pos() + delta)
    #             self.isMoving = True
    #             return
        #super().mouseMoveEvent(event)

    # def mouseReleaseEvent(self, event):
    #     if (not self.isMoving and
    #             self.textInteractionFlags() != Qt.TextEditorInteraction):
    #         self.setFocus()
    #         self.setSelected(True)
    #         self.setTextCursor(self.textCursor())
    #
    #     super().mouseReleaseEvent(event)
    #     self.startPos = None
    #     self.isMoving = False
