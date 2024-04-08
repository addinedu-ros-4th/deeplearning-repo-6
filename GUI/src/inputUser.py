# User face info 등록 페이지
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import *
import cv2
from PIL import Image
import threading
from PyQt5.QtWidgets import QMessageBox, QApplication , QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

from GUI.src.Camera import Camera
from GUI.src.Loading import Loading

from_class = uic.loadUiType("GUI/ui/inputUser.ui")[0]


class InputUserClass(QMainWindow, from_class) :
    
    def __init__(self ,main_window):
        super().__init__()
        self.main_window = main_window
        self.setupUi(self)
        
        self.setWindowTitle("사용자 등록")
        
        self.pixmap = QPixmap()
        
        self.cameraBtn.clicked.connect(self.clickCamera)
        self.isCameraOn = False
        self.camera = Camera(self)
        self.camera.demon = True
        self.count = 0
        self.loadingInstance = None
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        
        # 프레임 촬영 가능 여부
        self.ox = False
        
        # 카메라 내에 얼굴 존재 여부
        self.camera.signalNoFace.connect(self.noFace)
        
        self.camera.update.connect(self.updateCamera)
        self.userCamScreen.setText("camera를 켜주세요")
        
        # 녹화 종료 시그널
        self.camera.finishedRecording.connect(self.GIFLoading)
        
        self.frameStartBtn.hide()
        self.completeBtn.hide()
        self.frameStartBtn.clicked.connect(self.clickReady)
        
        # 종료되면 DB저장, 다음 페이지 전환
        self.completeBtn.clicked.connect(self.clickCompleteBtn)


    def clickCamera(self):
        # 촬영 중 X
        if self.isCameraOn == False:
            self.isCameraOn = True
            self.cameraBtn.setText("카메라 켜짐")
            self.frameStartBtn.show()
            
            self.cameraStart()
            
        # 촬영 중
        else:
            self.isCameraOn = False
            self.cameraBtn.setText("카메라 꺼짐")
            self.frameStartBtn.hide()
            
            self.cameraStop()
            
            
    def cameraStart(self):
        self.camera.isRunning = True
        self.camera.start()
        
           
    def cameraStop(self):
        self.count = 0
        self.camera.stop()
        
        self.pixmap = QPixmap()
        self.userCamScreen.setPixmap(self.pixmap)
        self.userCamScreen.setText("camera를 켜주세요")
    
    
    def updateCamera(self):
        retval, image = self.camera.video.read()
        
        if retval:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            h, w, c = image.shape
            qimage = QImage(image.data, w, h, w*c, QImage.Format_RGB888)
        
            pixmap = self.pixmap.fromImage(qimage)
            scaled_pixmap = pixmap.scaled(self.userCamScreen.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
            # 이미지를 중앙에 배치
            self.userCamScreen.setPixmap(scaled_pixmap)
            self.userCamScreen.setAlignment(Qt.AlignCenter)
        
        self.count += 1
    

    # 촬영 조건 확인
    def clickReady(self):
        result = QMessageBox.question(self, '사용자 등록 준비', '정면을 보셨나요?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if result == QMessageBox.Yes:
            result = QMessageBox.question(self, '사용자 등록 준비', '혼자 있으신가요?',
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            if result == QMessageBox.No:
                QMessageBox.warning(self, '사용자 등록 준비', '한 명만 인식할 수 있습니다.')
            else:
                self.success = self.GIFLoading()  # loading 메서드의 결과에 따라 complete 변수를 설정
        else:
            QMessageBox.warning(self, '사용자 등록 준비', '정면만 인식 가능합니다.')


    def GIFLoading(self):
        img_path = "GUI/data/countdown.gif"
        if self.camera.recordingCount < 2:
            self.loadingInstance = Loading(self, img_path, 521, 271, (30, 50), (521, 271), True)
            
            self.cameraBtn.setEnabled(False)
            self.frameStartBtn.setEnabled(False)
            
            # 3초 후에 로딩 인스턴스를 자동으로 삭제하는 타이머 설정
            QTimer.singleShot(2900, self.GIFLoading_finished)
        else:
            self.message.setText("촬영이 종료되었습니다.")
            self.frameStartBtn.hide()
            self.cameraBtn.hide()
            self.completeBtn.show()
        
        
    def GIFLoading_finished(self):
        # 로딩 인스턴스가 있으면 삭제하고 None으로 설정
        if self.loadingInstance is not None:
            self.loadingInstance.deleteLater()
            self.loadingInstance = None
            self.startRecord()


    def startRecord(self):
        # GIF 재생이 완료된 후 실행할 동작
        self.camera.startRecording()
        self.cameraBtn.setText("🔴REC")
        self.frameStartBtn.setText("등록 중")
        
        if self.camera.recordingCount == 1:
            self.message.setText("가까이 와주세요")
            threading.Timer(5, self.printMsg).start() # 3초뒤엔 다른 멘트 출력
        elif self.camera.recordingCount == 2:
            self.message.setText("멀리 가주세요")
            threading.Timer(5, self.printMsg).start() # 3초뒤엔 다른 멘트 출력
    
    
    # 촬영 조건 msg 출력
    def printMsg(self):
        self.message.setText("고개를 양옆으로 살짝씩 움직여주세요.")   
    
    
    def noFace(self):
        self.message.setText("얼굴이 인식되지 않습니다.")
    
    
    # 해당 사용자의 face 정보를 database에 insert
    def clickCompleteBtn(self):
        self.main_window.show_train_page()
        print("clicekc")
    
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    myWindows = WindowClass()
    
    myWindows.show()
    
    sys.exit(app.exec_())