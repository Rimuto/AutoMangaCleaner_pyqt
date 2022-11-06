from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from working_area_scene import QDMWorkingAreaScene
"""
PLAN IS:
    (DONE)  PAN & ZOOM
    (DONE)  SET IMAGE AS BACKGROUND
    (DONE)  DELETE ITEMS
    (DONE)  ADD EDITABLE TEXT ITEM
    (DONE)  BRUSH DRAWING
    LAYERS OR SMTH.? I DUNNO
    Можно рисовать на pixmap'e а не добавлять объекты на сцену, это должно помочь с лагами, если получиться 
    
    для поворота:
        находить уравнение нормали от точки до окружности
        находить точку пересечения нормали и окружности
        брать координаты курсора и соответственно им задавать координаты ручки на окружности
        НЕТ, еще лучше
            - ищем координаты вектора (мы знаем его начало и конец)
            - ищемкоординаты конца короткого вектора у которого мы знаем начало и длину
            
"""
class AddCommand(QUndoCommand):
    def __init__(self, item, scene):
        super().__init__()
        self.scene = scene
        self.item = item
        self.pos = item.scenePos()

    def undo(self):
        self.scene.removeItem(self.item)

    def redo(self):
        self.scene.addItem(self.item)
        self.item.setPos(self.pos)
        self.scene.drawingGroup.addToGroup(self.item)
        self.scene.clearSelection()


class QDMGraphicsView(QGraphicsView):
    def __init__(self, parent = None):
        super().__init__(parent)
    # scene settings
        self.grScene = QDMWorkingAreaScene()
        self.initUI()
        self.setScene(self.grScene)

        self.empty = True
        self.photo = QGraphicsPixmapItem()
        self.undoStack = QUndoStack(self)
    #text settings
        #fonts, color, outline etc.

    #brush drawing settings
        self.drawingMode = False
        self.is_drawing = False
        self.brushSize = 10
        self.brushColor = Qt.black
        self.lastPoint = QPoint()
        self.brush_line_pen = QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)


        self.initBrushCursor()
        # self.brushCursor = self.grScene.addEllipse(0, 0, self.brushSize, self.brushSize, QPen(Qt.NoPen), self.brushColor)
        # self.brushCursor.setFlag(QGraphicsItem.ItemIsMovable)
        # self.brushCursor.setZValue(-1)
        # self.brushCursor.setAcceptedMouseButtons(Qt.NoButton)

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

        # if self.drawingMode:
        #     self.brush = self.grScene.addEllipse(0, 0, self.brushSize, self.brushSize, QPen(Qt.NoPen), self.brushColor)
        #     self.brush.setFlag(QGraphicsItem.ItemIsMovable)
        #     self.brush.setAcceptedMouseButtons(Qt.NoButton)
        #     self.brush.setZValue(100)

    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def initBrushCursor(self):
        self.brushCursor = self.grScene.addEllipse(0, 0, self.brushSize, self.brushSize, QPen(Qt.NoPen), self.brushColor)
        self.brushCursor.setFlag(QGraphicsItem.ItemIsMovable)
        if self.drawingMode:
            self.brushCursor.setZValue(100)
        else:
            self.brushCursor.setZValue(-1)
        self.brushCursor.setAcceptedMouseButtons(Qt.NoButton)

    def setBrushSize(self, value):
        self.brushSize = value
        self.brush_line_pen = QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.hideBrushCursor()
        self.initBrushCursor()

    def setBrushColor(self, color):
        self.brushColor = color
        self.brush_line_pen = QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        self.hideBrushCursor()
        self.initBrushCursor()

    def addText(self):
        self.grScene.addText()

    def setDrawingMode(self, mode):
        if mode:
            self.setDragMode(QGraphicsView.NoDrag)
            self.drawingMode = True
            self.is_drawing = True
            self.showBrushCursor()
        else:
            self.setDragMode(QGraphicsView.RubberBandDrag)
            self.drawingMode = False
            self.is_drawing = False
            self.hideBrushCursor()

    def showBrushCursor(self):
        self.brushCursor.setVisible(True)
        self.brushCursor.setZValue(100)

    def hideBrushCursor(self):
        self.brushCursor.setZValue(-1)
        self.brushCursor.setVisible(False)

    def initialLinePath(self):
        self._path = QPainterPath()
        pen = self.brush_line_pen
        self._path_item = self.grScene.addPath(self._path, pen)

    def initialCirclePath(self):
        self.circle_path = QPainterPath()
        self.circle_path_item = self.grScene.addPath(self._path, QPen(Qt.NoPen), self.brushColor)

    def setMainImage(self, pixmapItem):
        self.grScene.setImage(pixmapItem)
        self.fitInView()

    def drawCircle(self, pos):
        self.circle_path.addEllipse(pos, self.brushSize/2, self.brushSize/2)
        self.circle_path_item.setPath(self.circle_path)
        self.grScene.drawingGroup.addToGroup(self.circle_path_item)

    def deleteCircle(self):
        self.grScene.removeItem(self.circle_path_item)
        self.grScene.drawingGroup.removeFromGroup(self.circle_path_item)
        self.circle_path_item = None

    def drawLine(self, pos):
        self._path.lineTo(self.mapToScene(pos))
        self._path_item.setPath(self._path)

    def mousePressEvent(self,  event):
        if self.drawingMode and (event.button() == Qt.LeftButton):
            self.initialLinePath()
            self.initialCirclePath()
            self.drawCircle(QPointF(self.mapToScene(event.pos()).toPoint()))
            self._path.moveTo(self.mapToScene(event.pos()))
            self._path_item.setPath(self._path)
        elif event.button() == Qt.LeftButton:
            self._mousePressed = True
            if self._isPanning:
                self.setCursor(Qt.ClosedHandCursor)
                self._dragPos = event.pos()
                event.accept()
            # else:
            #     super(QDMGraphicsView, self).mousePressEvent(event)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drawingMode:
            x = self.mapToScene(event.pos()).x()
            y = self.mapToScene(event.pos()).y()
            self.brushCursor.setPos(x - self.brushSize / 2, y - self.brushSize / 2)
        if(event.buttons() == Qt.LeftButton) & self.drawingMode:
            self.deleteCircle()
            self.drawLine(event.pos())
        elif self._mousePressed and self._isPanning:
            newPos = event.pos()
            diff = newPos - self._dragPos
            self._dragPos = newPos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())
            event.accept()
        #
        # else:
        #     super(QDMGraphicsView, self).mouseMoveEvent(event)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.drawingMode is True and self.circle_path_item is None:
                self.grScene.drawingGroup.addToGroup(self._path_item)
                self.undoStack.push(AddCommand(self._path_item, self.grScene))
            elif self.drawingMode is True and self.circle_path_item is not None:
                self.undoStack.push(AddCommand(self.circle_path_item, self.grScene))
            if event.modifiers() & Qt.ControlModifier:
                self.setCursor(Qt.OpenHandCursor)
            else:

                self._isPanning = False
                self.setCursor(Qt.ArrowCursor)
            self._mousePressed = False
        super(QDMGraphicsView, self).mouseReleaseEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_D:
            self.setDrawingMode(False)
        if event.key() == Qt.Key_S:
            self.setDrawingMode(True)
        if event.key() == Qt.Key_Z and event.modifiers() == Qt.ControlModifier:
            self.undoStack.undo()
        elif event.key() == Qt.Key_Y and event.modifiers() == Qt.ControlModifier:
            self.undoStack.redo()

        if event.key() == Qt.Key_Control:
            self.setDragMode(QGraphicsView.NoDrag)
            #print(self._mousePressed)
        if event.key() == Qt.Key_Control and not self._mousePressed:
            self.setDragMode(QGraphicsView.NoDrag)
            self.hideBrushCursor()
            self._isPanning = True
            self.drawingMode = False
            self.setCursor(Qt.OpenHandCursor)
        else:
            super(QDMGraphicsView, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Control:
            if self.is_drawing:
                #self.setDragMode(QGraphicsView.NoDrag)
                self.showBrushCursor()
                self.drawingMode = True
            else:
                self.setDragMode(QGraphicsView.RubberBandDrag)
            if not self._mousePressed:

                self._isPanning = False
                self.setCursor(Qt.ArrowCursor)
        elif event.key() == Qt.Key_Delete:
            for i in self.grScene.selectedItems():
                if i.item.textInteractionFlags() != Qt.TextEditorInteraction:
                    self.grScene.removeItem(i)
                    #self.deleteSelected()
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

    def fitInView(self, scale=True):
        rect = QRectF(self.grScene.mainImage.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.grScene.hasPhoto():
                unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
            self.zoom = 5

    def addImage(self, x, y, image, tag):
        self.grScene.addImage(x, y, image, tag)

    def delImage(self, tag):
        self.grScene.delImage(tag)

    def setTextHorizontalAlignment(self, alignment):
        for item in self.grScene.selectedItems():
            option = item.item.document().defaultTextOption()
            option.setAlignment(alignment)
            item.item.document().setDefaultTextOption(option)
            item.item.setTextWidth(item.boundingRect().width())

    def textHorizontalAlignLeft(self):
        self.setTextHorizontalAlignment(Qt.AlignLeft)

    def textHorizontalAlignRight(self):
        self.setTextHorizontalAlignment(Qt.AlignRight)

    def textHorizontalAlignCenter(self):
        self.setTextHorizontalAlignment(Qt.AlignCenter)

    def textHorizontalAlignJustify(self):
        self.setTextHorizontalAlignment(Qt.AlignJustify)

    def makeBold(self):
        for item in self.grScene.selectedItems():
            t = item.item.textCursor()
            if len(t.selectedText()) > 0:
                format = t.charFormat()
            else:
                t.select(QTextCursor.Document)
                format = t.charFormat()

            if format.fontWeight() == QFont.Normal:
                format.setFontWeight(QFont.Bold)
            elif format.fontWeight() == QFont.Bold:
                format.setFontWeight(QFont.Normal)
            t.setCharFormat(format)
            item.updateBoundingRect()

    def makeItalic(self):
        for item in self.grScene.selectedItems():
            t = item.item.textCursor()
            if len(t.selectedText()) > 0:
                format = t.charFormat()
            else:
                t.select(QTextCursor.Document)
                format = t.charFormat()

            if format.fontItalic():
                format.setFontItalic(False)
            else:
                format.setFontItalic(True)
            t.setCharFormat(format)
            item.updateBoundingRect()

    def makeUnderline(self):
        for item in self.grScene.selectedItems():
            t = item.item.textCursor()
            if len(t.selectedText()) > 0:
                format = t.charFormat()
            else:
                t.select(QTextCursor.Document)
                format = t.charFormat()

            if format.fontUnderline():
                format.setFontUnderline(False)
            else:
                format.setFontUnderline(True)
            t.setCharFormat(format)
            item.updateBoundingRect()


    def setFontColor(self, color):
        def do(t):
            format = t.charFormat()
            format.setForeground(color)
            t.setCharFormat(format)

        for item in self.grScene.selectedItems():
            t = item.item.textCursor()
            if len(t.selectedText()) > 0:
                do(t)
            else:
                t.select(QTextCursor.Document)
                do(t)
            item.updateBoundingRect()

    def setTextItemFont(self, font):
        def do(t):
            format = t.charFormat()
            pointSize = format.font().pointSize()
            font.setPointSize(pointSize)
            format.setFont(font)
            t.setCharFormat(format)

        for item in self.grScene.selectedItems():
            t = item.item.textCursor()
            if len(t.selectedText()) > 0:
                do(t)
            else:
                t.select(QTextCursor.Document)
                do(t)
            item.updateBoundingRect()

    def setFontSize(self, value):
        def do(t):
            format = t.charFormat()
            format.setFontPointSize(value)
            t.setCharFormat(format)

        for item in self.grScene.selectedItems():
            # add type check
            t = item.item.textCursor()
            if len(t.selectedText()) > 0:
                do(t)
            else:
                t.select(QTextCursor.Document)
                do(t)
            item.updateBoundingRect()

    def setLineHeight(self, value):
        for item in self.grScene.selectedItems():
            # add type check
            t = item.item.document()
            c = item.item.textCursor()

            for blockIndex in range(t.blockCount()):
                block = t.findBlock(blockIndex)
                f = block.blockFormat()
                f.setLineHeight(value, QTextBlockFormat.LineDistanceHeight)
                c.setBlockFormat(f)

            item.updateBoundingRect()

    def setRotationAngle(self, value):
        for item in self.grScene.selectedItems():
            item.setRotation(value)