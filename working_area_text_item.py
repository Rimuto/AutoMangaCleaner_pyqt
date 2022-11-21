from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class QDMTextItem(QGraphicsTextItem):
    def __init__(self, text):
        QGraphicsTextItem.__init__(self, text)
        self.startPos = None
        self.isMoving = False
        self.setSelected(False)
        self.setFlag(QGraphicsItem.ItemIsFocusable)

    def setFontSize(self, value):
        def do(t):
            format = t.charFormat()
            format.setFontPointSize(value)
            t.setCharFormat(format)
        # add type check
        t = self.textCursor()
        t.select(QTextCursor.Document)
        do(t)
        self.setTextWidth(-1)

    def boundingRect(self):
        return super().boundingRect() | QRectF(0, 0, 80, 25)

    def paint(self, painter, option, widget):
        option.state &= ~QStyle.State_Selected
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

    def hoverMoveEvent(self, moveEvent):
        super().hoverMoveEvent(moveEvent)

    def hoverLeaveEvent(self, moveEvent):
        self.setCursor(Qt.ArrowCursor)
        super().hoverLeaveEvent(moveEvent)
