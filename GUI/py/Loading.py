from PyQt5.QtWidgets import*
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QSize

FROM_CLASS_Loading = uic.loadUiType("GUI/ui/load.ui")[0]
#%% Loading Img
class Loading(QLabel, FROM_CLASS_Loading):
    finished = pyqtSignal() #GIF 종료 시그널
    
    def __init__(self,parent):
        super().__init__(parent)    
        self.setupUi(self) 
        self.center()
        self.show()
        
        self.labelWidth = 521  # QLabel 너비
        self.labelHeight = 300  # QLabel 높이
        self.countdown.setFixedSize(self.labelWidth, self.labelHeight)
        self.setGeometry(30, 40, 520, 281)
        
        # 동적 이미지 추가
        self.movie = QMovie('/home/addinedu/git_ws/deeplearning-repo-6/GUI/data/countdown.gif', QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setScaledSize(QSize(self.labelWidth, self.labelHeight))
        
        # QLabel에 동적 이미지 삽입
        self.countdown.setMovie(self.movie)
        
        self.movie.start()
        
        # GIF 재생이 끝나면 실행될 메서드 연결
        self.movie.finished.connect(self.onGIFFinished)
        
        # 윈도우 해더 숨기기
        # self.setWindowFlags(Qt.FramelessWindowHint)
    
    # 위젯 정중앙 위치
    def center(self):
        size=self.size()
        
        ph = 521
        pw = 281
        
        self.move(int(pw/2 - size.width()), int(ph/2 - size.height()))
        
    def onGIFFinished(self):
        self.finished.emit()

    
    