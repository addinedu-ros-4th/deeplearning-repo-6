from  PyQt5.QtCore import *
import os
import cv2
import numpy as np
import time
import threading
import cvlib as cv
from GUI.src.userSetting import global_user_name # 전역 변수 global_user_name을 가져옴

class Camera(QThread):                         
    update = pyqtSignal(np.ndarray)
    finishedRecording = pyqtSignal()
    signalNoFace = pyqtSignal()

    def __init__(self,parent=None):
        super().__init__()
        self.isRunning = False # 카메라 동작 플래그
        self.recording = False # 녹화 시작 플래그
        print(global_user_name)
        self.name = global_user_name # 전역 변수를 클래스 내에 사용
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
                    
                    if faces:
                        # 근접 촬영인지 떨어져서 촬영인지 판단
                        for index, ((x, y, x2, y2), conf) in enumerate(zip(faces, confidences)):
                            # 감지된 얼굴 영역을 잘라내서 저장
                            face_img = frame[y:y2, x:x2]
                            timestamp = int(time.time() * 2000)  # 밀리초 단위 타임스탬프
                            data_path = 'GUI/data/face'
                            
                            if not os.path.exists(data_path):
                                os.mkdir(data_path)
                            else:
                                filename = f'{data_path}/{self.mode}_{self.name}_frame_{timestamp}_{index}.jpg'
                                cv2.imwrite(filename, face_img)
                    else:
                        self.signalNoFace.emit()
                    
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
        