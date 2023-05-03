from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sys

class VideoWindow(QMainWindow):
    def __init__(self):
        super(VideoWindow, self).__init__()
        uic.loadUi("UI/app_ui.ui", self)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoWindow()
    window.show()
    sys.exit(app.exec_())
