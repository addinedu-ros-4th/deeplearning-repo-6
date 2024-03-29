from  PyQt5.QtCore import *
import cv2
import numpy as np
import time

class Camera(QThread):                         
    update = pyqtSignal(np.ndarray)
    
    def __init__(self, parent=None):
        super().__init__()
        self.isRunning = False # 카메라 동작 플래그
        self.recording = False # 녹화 시작 플래그
        self.name = 'gaeun'
    
    def run(self):
        self.video = cv2.VideoCapture(-1)
        if not self.video.isOpened():
            print("카메라를 열 수 없습니다.")
            return
        
        self.isRunning = True
        while self.isRunning:
            ret, frame = self.video.read()
            if ret:
                self.update.emit(frame)
                if self.recording:
                    # 녹화가 활성화된 경우 프레임 저장
                    timestamp = int(time.time() * 2000)  # 밀리초 단위 타임스탬프
                    filename = f'/home/addinedu/git_ws/deeplearning-repo-6/GUI/data/face/{self.name}_frame_{timestamp}.jpg'
                    cv2.imwrite(filename, frame)
            time.sleep(0.1)
        
        
    def stop(self):
        self.isRunning = False #카메라 동작 중지
        self.video.release()
    
    def startRecording(self):
        self.recording = True #녹화 시작
        
    def stopRecording(self):
        self.recording = False #녹화 중지
    