from PyQt5 import QtCore, QtGui, QtWidgets
from working_area_window import WorkingArea
from PyQt5.QtWidgets import *
from working_area_scene import QDMWorkingAreaScene
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import numpy as np
import cv2
import clean
import detect


labelsPath = "YOLOv4/obj.names"
cfgpath = "YOLOv4/yolov4-tiny-obj.cfg"
wpath = "YOLOv4/yolov4-tiny-obj_best.weights"

CFG = detect.config(cfgpath)
Weights = detect.weights(wpath)
nets = detect.load_model(CFG, Weights)

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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1108, 730)
        MainWindow.setMinimumSize(QtCore.QSize(1081, 691))

        self.current = 0
        self.model = QtGui.QStandardItemModel()
        self.contexts = {}

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.controls = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.controls.sizePolicy().hasHeightForWidth())
        self.controls.setSizePolicy(sizePolicy)
        self.controls.setMinimumSize(QtCore.QSize(1071, 101))
        self.controls.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.controls.setFrameShadow(QtWidgets.QFrame.Raised)
        self.controls.setObjectName("controls")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.controls)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_2.addWidget(self.pushButton_5, 0, 4, 1, 1)
        self.pushButton_6 = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_6.setFont(font)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout_2.addWidget(self.pushButton_6, 0, 5, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_2.addWidget(self.pushButton_7, 0, 6, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 0, 8, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_2.addWidget(self.pushButton_4, 0, 9, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_2.addWidget(self.checkBox, 0, 10, 1, 2)
        self.label_2 = QtWidgets.QLabel(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.spinBox = QtWidgets.QSpinBox(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spinBox.setFont(font)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout_2.addWidget(self.spinBox, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAutoFillBackground(False)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 2, 1, 1)
        self.spinBox_2 = QtWidgets.QSpinBox(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spinBox_2.setFont(font)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout_2.addWidget(self.spinBox_2, 1, 3, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_8.setFont(font)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_2.addWidget(self.pushButton_8, 1, 4, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_9.setFont(font)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout_2.addWidget(self.pushButton_9, 1, 5, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_10.setFont(font)
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout_2.addWidget(self.pushButton_10, 1, 6, 1, 1)
        self.pushButton_11 = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_11.setFont(font)
        self.pushButton_11.setObjectName("pushButton_11")
        self.gridLayout_2.addWidget(self.pushButton_11, 1, 7, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 10, 1, 1)
        self.spinBox_3 = QtWidgets.QSpinBox(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spinBox_3.setFont(font)
        self.spinBox_3.setObjectName("spinBox_3")
        self.gridLayout_2.addWidget(self.spinBox_3, 1, 11, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 2, 2, 1, 1)
        self.spinBox_4 = QtWidgets.QSpinBox(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.spinBox_4.setFont(font)
        self.spinBox_4.setObjectName("spinBox_4")
        self.gridLayout_2.addWidget(self.spinBox_4, 2, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 2, 10, 1, 1)
        self.fontComboBox = QtWidgets.QFontComboBox(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fontComboBox.setFont(font)
        self.fontComboBox.setObjectName("fontComboBox")
        self.gridLayout_2.addWidget(self.fontComboBox, 0, 0, 1, 4)
        self.verticalLayout.addWidget(self.controls)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(self.frame)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.frame_2 = QtWidgets.QFrame(self.splitter)
        self.frame_2.setMinimumSize(QtCore.QSize(231, 454))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")


        # self.checkBox_2 = QtWidgets.QCheckBox(self.frame_2)
        # self.checkBox_22 = QtWidgets.QCheckBox(self.frame_2)

        # self.horizontalLayout_3.addWidget(self.checkBox_22)


        self.frame_3 = QtWidgets.QFrame(self.splitter)
        self.frame_3.setMinimumSize(QtCore.QSize(811, 451))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")


        self.graphicsView = WorkingArea(self.frame_3)


        self.graphicsView.setObjectName("graphicsView")

        self.listWidget = QDMListWidget(self)

        self.horizontalLayout_3.addWidget(self.listWidget)

        self.horizontalLayout_2.addWidget(self.graphicsView)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.footer = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.footer.sizePolicy().hasHeightForWidth())
        self.footer.setSizePolicy(sizePolicy)
        self.footer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.footer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.footer.setObjectName("footer")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.footer)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.prevButton = QtWidgets.QPushButton(self.footer)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.prevButton.setFont(font)
        self.prevButton.setObjectName("prevButton")
        self.horizontalLayout.addWidget(self.prevButton)
        self.label = QtWidgets.QLabel(self.footer)
        font = QtGui.QFont()
        font.setPointSize(17)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.nextButton = QtWidgets.QPushButton(self.footer)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.nextButton.setFont(font)
        self.nextButton.setObjectName("nextButton")
        self.horizontalLayout.addWidget(self.nextButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addWidget(self.footer)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1108, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_image = QtWidgets.QAction(MainWindow)
        self.actionOpen_image.setObjectName("actionOpen_image")
        self.actionAdd_new_font = QtWidgets.QAction(MainWindow)
        self.actionAdd_new_font.setObjectName("actionAdd_new_font")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionOpen_image)
        self.menuFile.addAction(self.actionAdd_new_font)
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.nextButton.clicked.connect(lambda: self.shiftContext("forward"))
        self.prevButton.clicked.connect(lambda: self.shiftContext("backward"))
        self.actionOpen_image.triggered.connect(self.openFile)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_5.setText(_translate("MainWindow", "Bold"))
        self.pushButton_6.setText(_translate("MainWindow", "Italic"))
        self.pushButton_7.setText(_translate("MainWindow", "Underline"))
        self.pushButton_3.setText(_translate("MainWindow", "Add"))
        self.pushButton_4.setText(_translate("MainWindow", "Delete"))
        self.checkBox.setText(_translate("MainWindow", "Drawing Mode"))
        self.label_2.setText(_translate("MainWindow", "Size"))
        self.label_3.setText(_translate("MainWindow", "Height"))
        self.pushButton_8.setText(_translate("MainWindow", "Left"))
        self.pushButton_9.setText(_translate("MainWindow", "Center"))
        self.pushButton_10.setText(_translate("MainWindow", "Right"))
        self.pushButton_11.setText(_translate("MainWindow", "Justify"))
        self.label_4.setText(_translate("MainWindow", "Size"))
        self.label_6.setText(_translate("MainWindow", "Color"))
        self.label_5.setText(_translate("MainWindow", "Angle"))
        self.label_7.setText(_translate("MainWindow", "Color"))
        #self.checkBox_2.setText(_translate("MainWindow", "CheckBox"))
        self.prevButton.setText(_translate("MainWindow", "<-"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.nextButton.setText(_translate("MainWindow", "->"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_image.setText(_translate("MainWindow", "Open image"))
        self.actionAdd_new_font.setText(_translate("MainWindow", "Add new font"))
        self.actionSave.setText(_translate("MainWindow", "Save"))

    def createWorkingAreaScene(self, img):
        workingAreaScene = QDMWorkingAreaScene()
        workingAreaScene.setImage(QPixmap(self.convertToQImage(img)))
        return workingAreaScene

    def convertToQImage(self, img):
        height, width, channel = img.shape
        bytesPerLine = 3 * width
        qImg = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return qImg

    def shift(self, current):
        if len(self.contexts) > 0:
            self.listWidget.clear()
            if current > len(self.contexts) - 1:
                self.contexts[self.current]["scene"] = self.graphicsView.getScene()
                self.graphicsView.setScene(self.contexts[0]["scene"])
                self.listWidget.setList(self.contexts[0]["cleaned"])
                self.current = 0
            elif current < 0:
                self.contexts[self.current]["scene"] = self.graphicsView.getScene()
                self.graphicsView.setScene(self.contexts[len(self.contexts) - 1]["scene"])
                self.listWidget.setList(self.contexts[len(self.contexts) - 1]["cleaned"])
                self.current = len(self.contexts) - 1
            else:
                self.graphicsView.setScene(self.contexts[current]["scene"])
                self.listWidget.setList(self.contexts[current]["cleaned"])
                self.current = current

    def shiftContext(self, mode):
        if mode == "forward":
            self.shift(self.current + 1)
        elif mode == "backward":
            self.shift(self.current - 1)

    def next(self):
        self.shiftContext("forward")

    def prev(self):
        self.shiftContext("backward")

    def read_image(self, path):
        f = open(path, "rb")
        chunk = f.read()
        chunk_arr = np.frombuffer(chunk, dtype=np.uint8)
        img = cv2.imdecode(chunk_arr, cv2.IMREAD_COLOR)
        return img



    def openFile(self):
        # for i in range(5):
        #     icon_path = os.getcwd() + r"\32.png"
        #     text = f'{i}'
        #     icon = QtGui.QIcon(icon_path)
        #     item = QListWidgetItem(icon, text)
        #     item.setCheckState(Qt.Unchecked)
        #     self.listWidget.addItem(item)
        # self.listWidget.setDragDropMode(self.listWidget.InternalMove)
        # self.listWidget.setIconSize(QSize(300, 300))
        # self.listWidget.setSelectionMode(True)



        file, _ = QFileDialog.getOpenFileNames()
        if file:
            for i, file in enumerate(file):
                item = QtGui.QStandardItem(file)
                item.setData(file)
                self.model.appendRow(item)

                name = os.path.basename(item.data())
                print(item.data())
                img = self.read_image(item.data())
                res, bboxes = detect.detect(nets, img.copy())
                cl = []
                for j in bboxes:
                    x = j[0]
                    y = j[1]
                    w = j[2]
                    h = j[3]
                    cropped = img[y:y + h, x:x + w]

                    #ret, buffer = cv2.imencode('.png', cropped)

                    #qimage = QImage(buffer.data, cropped.shape[1], cropped.shape[0], QImage.Format_BGR888)
                    im = np.require(cropped, np.uint8, 'C')
                    cl.append({"x": x, "y": y, "img": self.convertToQImage(im), "checked": False})
                    cleaned = clean.remove(cropped)
                    img[y: y + h, x: x + w] = cleaned
                name, ext = os.path.splitext(name)
                workingAreaScene = self.createWorkingAreaScene(img)
                self.contexts[i] = {"scene": workingAreaScene, "cleaned": cl, "name": name, "ext": ext }
        self.listWidget.setList(self.contexts[0]["cleaned"])
        self.graphicsView.setScene(self.contexts[0]["scene"])
        # for index in range(self.model.rowCount()):
        #     item = self.model.item(index)
        #     print(item.data())