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

from GUI.src.Loading import Loading # GIF
from Face_recognize.face_save_learn import FaceImageCollectorAndRecognizerTrainer # Face 학습 model


from_class = uic.loadUiType("GUI/ui/train.ui")[0]
data_path = "GUI/data/face"
model_save_path = "Face_recognize/model"

class WindowClass(QMainWindow, from_class) :
    
    def __init__(self,parent = None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.setWindowTitle("사용자 등록 중입니다.")
        
        self.loadingInstance = None
        self.createDirectory(model_save_path)
        
        self.faceReconizer = FaceImageCollectorAndRecognizerTrainer(data_path, model_save_path)
        self.successBtn.hide()
        self.initGIF()
    
    
    # 폴더 생성
    def createDirectory(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print("Error: Failed to create the directory.")

    
    def showGIF(self):
        img_path = "GUI/data/ing.gif"
        # 학습 중 gif 객체 생성
        self.loadingInstance = Loading(self, img_path, 231, 221, (170, 250), (231, 221), True)
        
    
    def initGIF(self):
        img_path = "GUI/data/ing.gif"
        
        self.movie = QMovie(img_path)
        
        self.movie.setScaledSize(QSize(231, 221))
        self.gif.setMovie(self.movie)
    
        # GIF 재생 시작
        self.movie.start()
        
        self.show()
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    myWindows = WindowClass()
    
    myWindows.show()
    
    sys.exit(app.exec_())