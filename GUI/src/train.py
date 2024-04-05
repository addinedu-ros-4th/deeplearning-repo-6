# 얼굴 학습 페이지
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *
import os
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import pyqtSlot


from GUI.src.Loading import Loading # GIF
from Face_recognize.face_save_learn import FaceTrainer # Face 학습 model



from_class = uic.loadUiType("GUI/ui/train.ui")[0]
data_path = "GUI/data/face"
model_save_path = "Face_recognize/model"


class TrainClass(QMainWindow, from_class) :
     
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        
        self.createDirectory(model_save_path)
        
        self.main_window = main_window
        
        self.initUI()
        
        QTimer.singleShot(2000, self.train)
        
        
    def initUI(self):
        self.setWindowTitle("사용자 등록 중입니다.")
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
    
    
    # 훈련 시작
    def train(self):
        self.faceRecognizer = FaceTrainer(data_path, model_save_path)
       
        self.faceRecognizer.trainCompleted.connect(self.mySlot)
        self.faceRecognizer.train_model()
    
    
    # 훈련 완료 시그널 슬롯
    @pyqtSlot(bool)
    def mySlot(self):
        self.movie.stop() # GIF 종료
        self.gif.hide()
        self.successBtn.show() # 화면 전환 버튼 활성화
        self.successBtn.clicked.connect(self.goHome) # 화면 전환 함수 연결
        self.successBtn.setText("Home")
        self.label.setText("   당신만의 'Tier'가 생성되었습니다.")
        
        
    def goHome(self):
        # Change window
        self.main_window.show_main_page()
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    myWindows = TrainClass()
    
    myWindows.show()
    
    sys.exit(app.exec_())