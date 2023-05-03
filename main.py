from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5 import uic
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/mainwindow.ui", self)
        
        self.btnEnhanceImage.clicked.connect(self.openImageWindow)
        self.btnEnhanceVideo.clicked.connect(self.openVideoWindow)

    def openImageWindow(self):
        image_window = ImageWindow()
        image_window.show()

    def openVideoWindow(self):
        video_window = VideoWindow()
        video_window.show()

class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhance Image")
        self.setGeometry(200, 200, 400, 300)

class VideoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhance Video")
        self.setGeometry(200, 200, 400, 300)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
