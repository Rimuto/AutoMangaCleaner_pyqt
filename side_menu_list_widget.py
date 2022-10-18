from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class QDMListWidget(QListWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.setDragDropMode(self.InternalMove)
        self.setIconSize(QSize(300, 300))
        self.setSelectionMode(True)
        self.itemChanged.connect(self.item_changed)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if self.currentItem():
            if self.currentItem().checkState() == Qt.Checked:
                self.currentItem().setCheckState(Qt.Unchecked)
            elif self.currentItem().checkState() == Qt.Unchecked:
                self.currentItem().setCheckState(Qt.Checked)

    def deleteAll(self):
        self.clear()

    def setList(self, list):
        for i, listItem in enumerate(list):
            # icon_path = os.getcwd() + r"\32.png"
            # icon = QtGui.QIcon(icon_path)

            text = f'{i}'
            icon = QtGui.QIcon(QPixmap(listItem["img"]))
            item = QListWidgetItem(icon, text)
            if listItem["checked"]:
                item.setCheckState(Qt.Checked)
            elif not listItem["checked"]:
                item.setCheckState(Qt.Unchecked)

            self.addItem(item)

    def item_changed(self, item):
        currentContext = self.mainWindow.current
        if item.checkState() == Qt.Checked:
            itemTag = int(item.text())
            imgItem = self.mainWindow.contexts[currentContext]["cleaned"][itemTag]
            self.mainWindow.contexts[currentContext]["cleaned"][itemTag]["checked"] = True
            x = imgItem["x"]
            y = imgItem["y"]
            img = imgItem["img"]
            self.mainWindow.graphicsView.addImage(x, y, img, itemTag)
        elif item.checkState() == Qt.Unchecked:
            itemTag = int(item.text())
            self.mainWindow.contexts[currentContext]["cleaned"][itemTag]["checked"] = False
            self.mainWindow.graphicsView.delImage(itemTag)