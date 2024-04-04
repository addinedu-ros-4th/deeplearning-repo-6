from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import QMovie

FROM_CLASS_Loading = uic.loadUiType("GUI/ui/load.ui")[0]

class Loading(QLabel, FROM_CLASS_Loading):
    finished = pyqtSignal()  # GIF 종료 시그널

    def __init__(self, parent, img_path, labelWidth=231, labelHeight=221, windowPosition=(170,250), windowSize=(231,221), hideWindowHeader=False):
        super().__init__(parent)
        self.setupUi(self)
        self.img_path = img_path
        self.labelWidth = labelWidth
        self.labelHeight = labelHeight
        self.windowPosition = windowPosition
        self.windowSize = windowSize
        self.initUI(hideWindowHeader)
        
        
    def initUI(self, hideWindowHeader):
        self.countdown.setFixedSize(self.labelWidth, self.labelHeight)
        self.setGeometry(*self.windowPosition, *self.windowSize)
        
        # 동적 이미지 추가
        self.movie = QMovie(self.img_path, QByteArray(), self)
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setScaledSize(QSize(self.labelWidth, self.labelHeight))
        self.countdown.setMovie(self.movie)
        self.movie.start()
        self.movie.finished.connect(self.onGIFFinished)
        
        if hideWindowHeader:
            self.setWindowFlags(Qt.FramelessWindowHint)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def onGIFFinished(self):
        self.finished.emit()
