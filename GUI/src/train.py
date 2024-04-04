# 얼굴 학습 페이지
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *
import cv2
import os
from PIL import Image
import threading

from GUI.src.Loading import Loading
from Face_recognize.face_recognize import FaceRecognizer
from Face_recognize.face_save_learn import FaceImageCollectorAndRecognizerTrainer


from_class = uic.loadUiType("GUI/ui/train.ui")[0]
folder_path = "GUI/data/face"
model_save_path = "Face_rocognize/model"

class WindowClass(QMainWindow, from_class) :
    
    def __init__(self,parent = None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.setWindowTitle("사용자 등록 중입니다.")
        
        self.pixmap = QPixmap()
        
        self.createDirectory(model_save_path)
        
        self.faceReconizer = FaceRecognizer()

    
    # 폴더 생성
    def createDirectory(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print("Error: Failed to create the directory.")

    
    def gif 
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    myWindows = WindowClass()
    
    myWindows.show()
    
    sys.exit(app.exec_())