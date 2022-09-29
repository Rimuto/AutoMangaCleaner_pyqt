import sys
from PyQt5.QtWidgets import *
from ui import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from working_area_window import WorkingArea

if __name__ == "__main__":
    # app = QApplication(sys.argv)
    # window = WorkingArea()
    # sys.exit(app.exec_())



    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())




