from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QLabel,
    QTextEdit,
    QPushButton,
    QFileDialog,
)

# from models.ESRGAN import image_enhancer as ie
from ..models.ESRGAN import image_enhancer as ie
from PyQt5 import uic
import sys
import os


class imageWindow(QMainWindow):
    def __init__(self):
        super(imageWindow, self).__init__()

        uic.loadUi("UI/imagewindow.ui", self)

        # Defining custom widgets for vriddhi (si- select image, sf- select folder)
        self.button_si = self.findChild(QPushButton, "pushButton")
        self.path_si = self.findChild(QTextEdit, "textEdit")
        self.cancel_si = self.findChild(QPushButton, "pushButton_2")
        self.button_sf = self.findChild(QPushButton, "pushButton_3")
        self.cwd = self.findChild(QPushButton, "pushButton_6")
        self.path_sf = self.findChild(QTextEdit, "textEdit_2")
        self.cancel_sf = self.findChild(QPushButton, "pushButton_4")
        self.execute = self.findChild(QPushButton, "pushButton_5")
        self.outputlabel = self.findChild(QLabel, "label_3")

        # Actions:
        self.button_si.clicked.connect(self.image_get)
        self.cancel_si.clicked.connect(self.path_si_clear)

        self.button_sf.clicked.connect(self.folder_get)
        self.cwd.clicked.connect(self.cwd_store)
        self.cancel_sf.clicked.connect(self.path_sf_clear)

        self.execute.clicked.connect(self.run)

        # show app
        self.show()

    # Functions:
    def image_get(self):
        file_path = QFileDialog.getOpenFileName(
            self,
            "Selected images will be enhanced:",
            ".",
            "Image Files (*.png *.jpg *.jpeg)",
        )
        if file_path:
            self.path_si.setText(file_path[0])
        global cv_file
        cv_file = self.path_si.toPlainText()

    def path_si_clear(self):
        self.path_si.setText("")

    def folder_get(self):
        folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")
        if folder_path:
            self.path_sf.setText(folder_path)
        global cv_folder
        cv_folder = self.path_sf.toPlainText()

    def cwd_store(self):
        folder_path = os.getcwd()
        if folder_path:
            self.path_sf.setText(folder_path)
        global cv_folder
        cv_folder = self.path_sf.toPlainText()

    def path_sf_clear(self):
        self.path_sf.setText("")

    def run(self):
        try:
            # runs model after app execution is terminated
            model_path = "models/ESRGAN/models/RRDB_ESRGAN_x4.pth"
            images_path = cv_file
            ie.enhance_image(images_path, model_path, output_path=cv_folder)
            self.outputlabel.setText(f"Enhancement Successful!!!!")
        except:
            self.outputlabel.setText(f"Invalid selections")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ImageWindow = imageWindow()
    app.exec_()
