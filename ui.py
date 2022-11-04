from PyQt5 import QtCore, QtGui, QtWidgets
from working_area_window import WorkingArea
from PyQt5.QtWidgets import *
from working_area_scene import QDMWorkingAreaScene
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from side_menu_list_widget import QDMListWidget
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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1110, 748)
        MainWindow.setMinimumSize(QtCore.QSize(1081, 691))


        self.current = 0
        self.model = QtGui.QStandardItemModel()
        self.contexts = {}


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 0)
        self.verticalLayout.setSpacing(0)
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
        self.height_lbl = QtWidgets.QLabel(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.height_lbl.setFont(font)
        self.height_lbl.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.height_lbl.setAutoFillBackground(False)
        self.height_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.height_lbl.setObjectName("height_lbl")
        self.gridLayout_2.addWidget(self.height_lbl, 1, 2, 1, 1)
        self.angle_spn = QtWidgets.QSpinBox(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.angle_spn.setFont(font)
        self.angle_spn.setObjectName("angle_spn")
        self.gridLayout_2.addWidget(self.angle_spn, 2, 3, 1, 1)
        self.height_spn = QtWidgets.QSpinBox(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.height_spn.setFont(font)
        self.height_spn.setObjectName("height_spn")
        self.height_spn.setRange(1, 100)
        self.height_spn.setValue(1)
        self.gridLayout_2.addWidget(self.height_spn, 1, 3, 1, 1)
        self.alig_right_btn = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.alig_right_btn.setFont(font)
        self.alig_right_btn.setObjectName("alig_right_btn")
        self.gridLayout_2.addWidget(self.alig_right_btn, 1, 6, 1, 1)
        self.brush_color_lbl = QtWidgets.QLabel(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.brush_color_lbl.setFont(font)
        self.brush_color_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.brush_color_lbl.setObjectName("brush_color_lbl")
        self.gridLayout_2.addWidget(self.brush_color_lbl, 2, 10, 1, 1)
        self.alig_center_btn = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.alig_center_btn.setFont(font)
        self.alig_center_btn.setObjectName("alig_center_btn")
        self.gridLayout_2.addWidget(self.alig_center_btn, 1, 5, 1, 1)
        self.bold_btn = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.bold_btn.setFont(font)
        self.bold_btn.setObjectName("bold_btn")
        self.gridLayout_2.addWidget(self.bold_btn, 0, 4, 1, 1)
        self.fontComboBox = QtWidgets.QFontComboBox(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fontComboBox.setFont(font)
        self.fontComboBox.setObjectName("fontComboBox")
        self.gridLayout_2.addWidget(self.fontComboBox, 0, 0, 1, 4)
        self.font_size_lbl = QtWidgets.QLabel(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.font_size_lbl.setFont(font)
        self.font_size_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.font_size_lbl.setObjectName("font_size_lbl")
        self.gridLayout_2.addWidget(self.font_size_lbl, 1, 0, 1, 1)
        self.font_color_lbl = QtWidgets.QLabel(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.font_color_lbl.setFont(font)
        self.font_color_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.font_color_lbl.setObjectName("font_color_lbl")
        self.gridLayout_2.addWidget(self.font_color_lbl, 2, 0, 1, 1)
        self.alig_left_btn = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.alig_left_btn.setFont(font)
        self.alig_left_btn.setObjectName("alig_left_btn")
        self.gridLayout_2.addWidget(self.alig_left_btn, 1, 4, 1, 1)
        self.alig_justify_btn = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.alig_justify_btn.setFont(font)
        self.alig_justify_btn.setObjectName("alig_justify_btn")
        self.gridLayout_2.addWidget(self.alig_justify_btn, 1, 7, 1, 1)
        self.underline_btn = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.underline_btn.setFont(font)
        self.underline_btn.setObjectName("underline_btn")
        self.gridLayout_2.addWidget(self.underline_btn, 0, 6, 1, 1)
        self.delete_text_btn = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.delete_text_btn.setFont(font)
        self.delete_text_btn.setObjectName("delete_text_btn")
        self.gridLayout_2.addWidget(self.delete_text_btn, 0, 9, 1, 1)
        self.font_size_spn = QtWidgets.QSpinBox(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.font_size_spn.setFont(font)
        self.font_size_spn.setRange(1, 250)
        self.font_size_spn.setValue(10)
        self.font_size_spn.setObjectName("font_size_spn")
        self.gridLayout_2.addWidget(self.font_size_spn, 1, 1, 1, 1)
        self.brush_size_lbl = QtWidgets.QLabel(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.brush_size_lbl.setFont(font)
        self.brush_size_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.brush_size_lbl.setObjectName("brush_size_lbl")
        self.gridLayout_2.addWidget(self.brush_size_lbl, 1, 10, 1, 1)
        self.add_text_btn = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.add_text_btn.setFont(font)
        self.add_text_btn.setObjectName("add_text_btn")
        self.gridLayout_2.addWidget(self.add_text_btn, 0, 8, 1, 1)
        self.brush_size_spn = QtWidgets.QSpinBox(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.brush_size_spn.setFont(font)
        self.brush_size_spn.setObjectName("brush_size_spn")
        self.gridLayout_2.addWidget(self.brush_size_spn, 1, 11, 1, 1)
        self.drawing_mode_chk = QtWidgets.QCheckBox(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.drawing_mode_chk.setFont(font)
        self.drawing_mode_chk.setObjectName("drawing_mode_chk")
        self.gridLayout_2.addWidget(self.drawing_mode_chk, 0, 10, 1, 2)
        self.angle_lbl = QtWidgets.QLabel(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.angle_lbl.setFont(font)
        self.angle_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.angle_lbl.setObjectName("angle_lbl")
        self.gridLayout_2.addWidget(self.angle_lbl, 2, 2, 1, 1)
        self.italic_btn = QtWidgets.QPushButton(self.controls)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.italic_btn.setFont(font)
        self.italic_btn.setObjectName("italic_btn")
        self.gridLayout_2.addWidget(self.italic_btn, 0, 5, 1, 1)

        self.text_color_picker = QtWidgets.QPushButton(self.controls)
        self.text_color_picker.setText("")
        self.text_color_picker.setObjectName("text_color_picker")
        self.gridLayout_2.addWidget(self.text_color_picker, 2, 1, 1, 1)
        self.brush_color_picker = QtWidgets.QPushButton(self.controls)
        self.brush_color_picker.setText("")
        self.brush_color_picker.setObjectName("brush_color_picker")
        self.gridLayout_2.addWidget(self.brush_color_picker, 2, 11, 1, 1)

        self.verticalLayout.addWidget(self.controls)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(-1, -1, -1, 1)
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
        self.footer.setMaximumSize(QtCore.QSize(16777215, 50))
        self.footer.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.footer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.footer.setObjectName("footer")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.footer)
        self.horizontalLayout.setContentsMargins(-1, 1, -1, 1)
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
        font.setPointSize(15)
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
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1110, 26))
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

        self.angle_spn.setRange(-360, 360)
        self.nextButton.clicked.connect(lambda: self.shiftContext("forward"))
        self.prevButton.clicked.connect(lambda: self.shiftContext("backward"))
        self.actionOpen_image.triggered.connect(self.openFile)
        self.add_text_btn.clicked.connect(self.addText)
        self.delete_text_btn.clicked.connect(self.deleleteSelected)
        self.fontComboBox.currentFontChanged.connect(self.setTextItemFont)
        self.font_size_spn.valueChanged.connect(self.setFontSize)
        self.height_spn.valueChanged.connect(self.setLineHeight)
        self.angle_spn.valueChanged.connect(self.setRotationAngle)
        self.text_color_picker.clicked.connect(self.setFontColor)
        self.brush_color_picker.clicked.connect(self.setBrushColor)
        self.drawing_mode_chk.clicked.connect(self.setDrawingMode)
        self.brush_size_spn.valueChanged.connect(self.setBrushSize)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.height_lbl.setText(_translate("MainWindow", "Height"))
        self.alig_right_btn.setText(_translate("MainWindow", "Right"))
        self.brush_color_lbl.setText(_translate("MainWindow", "Color"))
        self.alig_center_btn.setText(_translate("MainWindow", "Center"))
        self.bold_btn.setText(_translate("MainWindow", "Bold"))
        self.font_size_lbl.setText(_translate("MainWindow", "Size"))
        self.font_color_lbl.setText(_translate("MainWindow", "Color"))
        self.alig_left_btn.setText(_translate("MainWindow", "Left"))
        self.alig_justify_btn.setText(_translate("MainWindow", "Justify"))
        self.underline_btn.setText(_translate("MainWindow", "Underline"))
        self.delete_text_btn.setText(_translate("MainWindow", "Delete"))
        self.brush_size_lbl.setText(_translate("MainWindow", "Size"))
        self.add_text_btn.setText(_translate("MainWindow", "Add"))
        self.drawing_mode_chk.setText(_translate("MainWindow", "Drawing Mode"))
        self.angle_lbl.setText(_translate("MainWindow", "Angle"))
        self.italic_btn.setText(_translate("MainWindow", "Italic"))
        self.prevButton.setText(_translate("MainWindow", "<-"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.nextButton.setText(_translate("MainWindow", "->"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_image.setText(_translate("MainWindow", "Open image"))
        self.actionAdd_new_font.setText(_translate("MainWindow", "Add new font"))
        self.actionSave.setText(_translate("MainWindow", "Save"))


    def setDrawingMode(self):
        if self.drawing_mode_chk.checkState() == Qt.Checked:
            self.graphicsView.setDrawingMode(True)
        elif self.drawing_mode_chk.checkState() == Qt.Unchecked:
            self.graphicsView.setDrawingMode(False)

    def setFontColor(self):
        color = self.openColorPickerDialog()
        if color != 0:
            self.text_color_picker.setStyleSheet(f'QPushButton {{background-color: {color.name()};}}')
            self.graphicsView.setTextColor(color)

    def setBrushSize(self, value):
        self.graphicsView.setBrushSize(value)

    def setBrushColor(self):
        color = self.openColorPickerDialog()
        if color != 0:
            self.brush_color_picker.setStyleSheet(f'QPushButton {{background-color: {color.name()};}}')
            self.graphicsView.setBrushColor(color)

    def openColorPickerDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            print(color.name())
            return color
        return 0


    def setRotationAngle(self, value):
        self.graphicsView.setRotationAngle(value)

    def setLineHeight(self, value):
        self.graphicsView.setLineHeight(value)

    def setFontSize(self, value):
        self.graphicsView.setTextFontSize(value)

    def setTextItemFont(self):
        font = self.fontComboBox.currentFont()
        self.graphicsView.setTextFont(font)

    def deleleteSelected(self):
        self.graphicsView.deleteSelectedObject()

    def addText(self):
        self.graphicsView.addText()

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