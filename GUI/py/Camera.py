from  PyQt5.QtCore import *
import cv2
import numpy as np
import time
import threading
from Loading import Loading
import cvlib as cv

class Camera(QThread):                         
    update = pyqtSignal(np.ndarray)
    finishedRecording = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__()
        self.isRunning = False # 카메라 동작 플래그
        self.recording = False # 녹화 시작 플래그
        self.name = 'hyegyeong'
        self.mode = 'close' # 첫 촬영은 근접촬영
        self.recordingCount = 0 #녹화 순서 지정을 위한 횟수 추적

    
    def run(self):
        self.video = cv2.VideoCapture(-1)
        
        if not self.video.isOpened():
            print("카메라를 열 수 없습니다.")
            return
        
        self.isRunning = True
        
        while self.isRunning:
            ret, frame = self.video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 그레이스케일 변환
    
            if ret:
                self.update.emit(frame)
                
                if self.recording:
                    # 녹화가 활성화된 경우 프레임 저장
                    # 얼굴 찾기
                    faces, confidences = cv.detect_face(frame)
                    timestamp = int(time.time() * 2000)  # 밀리초 단위 타임스탬프
                    
                    # 근접 촬영인지 떨어져서 촬영인지 판단
                    if self.mode == 'close':
                        filename = f'/home/addinedu/git_ws/deeplearning-repo-6/GUI/data/face/{self.mode}_{self.name}_frame_{timestamp}.jpg'
                    elif self.mode == 'far':
                        filename = f'/home/addinedu/git_ws/deeplearning-repo-6/GUI/data/face/{self.mode}_{self.name}_frame_{timestamp}.jpg'
                    else:
                        print("해당 모드가 없습니다.")
                        break
                    
                    for (x, y, x2, y2), conf in zip(faces, confidences):
                        # 감지된 얼굴 영역을 잘라내서 저장
                        face_img = frame[y:y2, x:x2]  # 얼굴 영역을 잘라냄
                
                    cv2.imwrite(filename, face_img)
                    
            time.sleep(0.1)
        
        
    def stop(self):
        if self.recording: #녹화 중지
            self.stopRecording()
            
        self.isRunning = False #카메라 동작 중지
        self.video.release()
    
    
    def startRecording(self):
        self.recording = True #녹화 시작
        self.recordingCount += 1
        
        if self.recordingCount == 1:
            threading.Timer(10, self.stopRecording).start() # 10초 녹화
        elif self.recordingCount == 2:
            self.mode = 'far'
            threading.Timer(10, self.stop).start() # 녹화 종료
        else:
            self.stop() #촬영이 끝나면 카메라, 녹화 종료
        
        
    def stopRecording(self):
        self.recording = False #녹화 중지
        self.finishedRecording.emit()
    
    
    # 카운트다운이 끝나면 모드변경 후 촬영 재개
    def recMode(self, signal):
        self.mode = 'far'
        print(f"모드 변경: {self.mode}, 녹화 재개")
        
        self.startRecording()
        