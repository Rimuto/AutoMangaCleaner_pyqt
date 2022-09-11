import sys
from PyQt5.QtWidgets import *

from working_area_window import WorkingArea

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = WorkingArea()

    sys.exit(app.exec_())