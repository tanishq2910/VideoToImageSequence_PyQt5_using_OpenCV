from PyQt5.QtWidgets import QMainWindow,QApplication, QLabel, QTextEdit,QPushButton, QFileDialog
from PyQt5 import uic
from models.ESRGAN import image_enhancer as ie
from video_processing import img_to_vid as i2v
from video_processing import vid_to_img as v2i
import sys
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("UI/mainwindow.ui", self)
        
        self.btnEnhanceImage.clicked.connect(self.openImageWindow)
        self.btnEnhanceVideo.clicked.connect(self.openVideoWindow)

    def openImageWindow(self):
        image_window = ImageWindow()
        image_window.show()

    def openVideoWindow(self):
        # self.close()
        # video_window = VideoWindow()
        # video_window.show()
        self.window= QMainWindow()
        self.window = VideoWindow()
        #self.window.textEdit.setText(cv_folder)
        self.window.show()
class ImageWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhance Image")
        self.setGeometry(200, 200, 400, 300)

class VideoWindow(QMainWindow):
    fps=None
    def __init__(self):
        # super(VideoWindow, self).__init__()
        super(VideoWindow, self).__init__()
        uic.loadUi("UI/app_ui.ui", self)
        
        #Defining custom widgets for vriddhi (sv- select video, sf- select folder)
        self.button_sv = self.findChild(QPushButton,"pushButton")
        self.path_sv = self.findChild(QTextEdit,"textEdit")
        self.cancel_sv = self.findChild(QPushButton,"pushButton_2")
        self.button_sf = self.findChild(QPushButton,"pushButton_3")
        self.cwd = self.findChild(QPushButton,"pushButton_6")
        self.path_sf = self.findChild(QTextEdit,"textEdit_2")
        self.cancel_sf = self.findChild(QPushButton,"pushButton_4")
        self.execute = self.findChild(QPushButton,"pushButton_5")
        self.outputlabel = self.findChild(QLabel,"label_3")

        #Actions:
        self.button_sv.clicked.connect(self.video_get)#actions for both select video and path_sv are included
        self.cancel_sv.clicked.connect(self.path_sv_clear)

        self.button_sf.clicked.connect(self.folder_get)#actions for both select folder and path_sf are included
        self.cwd.clicked.connect(self.cwd_store)#path_sf is cwd
        self.cancel_sf.clicked.connect(self.path_sf_clear)

        self.execute.clicked.connect(self.run)#using both path saved, program is run

        # #show app
        # self.show()

        #Functions:
    def video_get(self):
        file_path = QFileDialog.getOpenFileName(self, "Selected video will be converted into image sequence:","C:\\Users\\asus\\Desktop\\Video", "Video(*.mp4)")

        if file_path:
            self.path_sv.setText(file_path[0])
        global cv_file
        cv_file= self.path_sv.toPlainText()
    
    def path_sv_clear(self):
        self.path_sv.setText("")

    def folder_get(self):
        folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")
        if folder_path:
            self.path_sf.setText(folder_path)
        global cv_folder 
        cv_folder= self.path_sf.toPlainText()

    def cwd_store(self):
        folder_path =os.getcwd()
        if folder_path:
            self.path_sf.setText(folder_path)
        global cv_folder
        cv_folder= self.path_sf.toPlainText()
    
    def path_sf_clear(self):
        self.path_sf.setText("")

    def run(self):
        try:
            v2i.vid_to_img(cv_file, cv_folder)
            self.outputlabel.setText(f'Saved sucessfully!!!!')
            # runs model after app execution is terminated
            model_path = 'models/ESRGAN/models/RRDB_ESRGAN_x4.pth'
            images_path = cv_folder+"/*"
            ie.enhance_image(images_path, model_path)
            # enhanced images converted to video
            i2v.img_to_vid(VideoWindow.fps)
            self.outputlabel.setText(f'Enhancement Successful!!!!')
        except:
            self.outputlabel.setText(f'Invalid selections')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
