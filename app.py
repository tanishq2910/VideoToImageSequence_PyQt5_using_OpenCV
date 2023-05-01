from PyQt5.QtWidgets import QMainWindow,QApplication, QLabel, QTextEdit,QPushButton, QFileDialog
from models.ESRGAN import image_enhancer as ie
from PyQt5 import uic
import sys
import os
import cv2

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

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

        #show app
        self.show()

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
            cap= cv2.VideoCapture(cv_file)
            i=0
            path=cv_folder
            while(cap.isOpened()):
                ret, frame = cap.read()
                if ret == False:
                    break
                #cv2.imwrite(os.path.join(path , 'waka.jpg'), img)
                cv2.imwrite(os.path.join(path,'Snap'+str(i)+'.jpg'),frame)
                i+=1
            cap.release()
            cv2.destroyAllWindows()
        #self.outputlabel.setText(f'Video taken was: {cv_file}')
        #print(type(cv_file))
        #print(cv_file)
            self.outputlabel.setText(f'Saved sucessfully!!!!')
            
            # runs model after app execution is terminated
            images_path = cv_folder+"/*"
            model_path = 'models/ESRGAN/models/RRDB_ESRGAN_x4.pth'
            ie.enhance_image(images_path, model_path)
            
            self.outputlabel.setText(f'Enhanced images saved!!!')
            
        except:
            self.outputlabel.setText(f'Invalid selections')


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
