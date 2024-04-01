import os
import threading
from time import sleep
import signal
from mic_amp import AudioAmplifier
from mic import VoiceRecorder
from gpt import ChatGPTAssistant, ModelConfigThread #, ChatThread
import time
import threading
from PyQt5 import QtWidgets,uic
from googleapi import FileMonitor, AudioTranscriber
from PyQt5.QtCore import pyqtSignal, QThread, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QImage, QPixmap
import cv2

import speech_recognition as sr
import os
from datetime import datetime
from gtts import gTTS
import pygame

#ui = "/home/ito/amr_ws/mechine learing/project/mic/finetuning/SR_gui.ui"
ui = "/home/djy0404/amr_ws/project/communication_model/test_files/GUI/SR_gui.ui"
# .ui 파일을 파이썬 코드로 변환
Ui_MainWindow, QtBaseClass = uic.loadUiType(ui)

class Signal(QObject):
    mike_off = pyqtSignal()
    userTextChanged = pyqtSignal(str)

class Mike_thread(QThread):
    result_text = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        recognizer = sr.Recognizer()

        print("마이크 입력을 시작합니다.")
        with sr.Microphone() as source:
            while self.running:
                try:
                    print("음성 입력을 기다리는 중...")
                    audio_data = recognizer.listen(source)
                    """
                    # 현재 시간을 기반으로 파일 이름 생성
                    now = datetime.now()
                    filename = f"audio_{now.strftime('%Y%m%d_%H%M%S')}.wav"
                    file_path = os.path.join(os.getcwd(), filename)

                    # 음성 녹음 파일 저장
                    with open(file_path, "wb") as f:
                        f.write(audio_data.get_wav_data())
                        print(f"음성 파일이 '{file_path}'에 저장되었습니다.")
                    """
                    text = recognizer.recognize_google(audio_data, language="ko-KR")
                    self.result_text.emit(text)

                    
                except sr.UnknownValueError:
                    text = "음성을 인식할 수 없습니다."
                    self.result_text.emit(text)
                except sr.RequestError:
                    print("Google Web API 요청이 실패했습니다. 에러 메시지:")
                except sr.WaitTimeoutError:
                    print("녹음 1번이 끝남")

                if not self.running:
                    break

        self.finished.emit()

class Mike_thread2(QThread):
    result_text = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.running = True

    def stop(self):
        self.running = False

    def run(self):
        vr = VoiceRecorder()
        recognizer = sr.Recognizer()
        print("마이크 입력을 시작합니다.")
        while self.running:
            vr.start_recording()
            vr.save_recording()
            audio_path = vr.get_audio_path()
            
            with sr.AudioFile(audio_path) as source:
                audio_data = recognizer.record(source)
                try:
                    # Google 웹 API를 사용하여 음성을 텍스트로 변환
                    text = recognizer.recognize_google(audio_data, language="ko-KR")
                    print("인식된 텍스트:", text)
                    self.result_text.emit(text)
     
                except sr.UnknownValueError:
                    print("음성을 인식할 수 없습니다.")
                except sr.RequestError:
                    print("Google 웹 API 요청이 실패했습니다. 에러 메시지:")

            

        self.finished.emit()

class WebCamThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)
    def run(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()  # 웹캠에서 프레임 읽기
            if ret:
                # OpenCV에서 읽은 이미지를 PyQt용 QImage으로 변환
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)

                # 이미지 변경 신호를 발생시켜 메인 스레드로 이미지 전달
                self.change_pixmap_signal.emit(qt_image)
            else:
                print("Failed to receive frame")
                break

        cap.release()  # 웹캠 연결 해제

class ChatModule(QtWidgets.QMainWindow):
    def __init__(self,parent = None):
        super(ChatModule, self).__init__(parent)

        # 데이터 경로 설정
        self.data_path = "/home/ito/amr_ws/mechine learing/project/mic/mic_data/"

        # 모델 구성 정의
        self.model_configs = [
            {"model": "gpt-3.5-turbo", "system_message": "반말을 사용하고, 감정적이고 친화적인 경향을 가지며, 친근하고 상냥한 말투로 해줘.", "assistant_message": "좋은 하루 보내!"},
            {"model": "gpt-3.5-turbo", "system_message": "반말을 사용하고, 주로 논리적이고 분석적인 성향을 가지고 있으며, 객관적인 사고와 문제 해결에 뛰어나.", "assistant_message": "무슨 문제 있어?"},
            {"model": "gpt-3.5-turbo", "system_message": "딱딱한 말투를 사용하고, 자신이 저지른 악행에 대해 합리화를 잘할뿐더러 타인과 타협도 잘 하지 않는 완고한 성격이야", "assistant_message": "나는 필연적인 존재다."},
        ]

        # UI 요소 생성을 메인 스레드에서 수행
        self.create_ui_elements()
        
        # 웹캠 시작 시 스레드 실행
        self.webcam_thread = WebCamThread()
        self.webcam_thread.change_pixmap_signal.connect(self.update_image)  # 이미지 업데이트 신호 연결
        self.webcam_thread.start()  # 웹캠 스레드 시작
        
        # 마이크 상태 변경 시그널
        self.signals = Signal()

        # 마이크 버튼 클릭 이벤트 핸들러 연결
        self.ui.btn_Mike_on.clicked.connect(self.on_mike_button_clicked)

        # 마이크 상태 변수
        self.mike_on = False
        self.mike_status = False
        self.mike_thread = None

        # 음성 출력 버튼 이벤트 핸들러 연결
        self.ui.btn_Output.clicked.connect(self.voice_button_clicked)

        self.selected_model_index = 1  # 초기 모델 인덱스 설정
        
        # ChatGPTAssistant 인스턴스 생성
        self.assistant = ChatGPTAssistant(self.model_configs)
        
        # 모델 구성 업데이트 스레드 시작
        self.start_model_config_thread()
        
        # 모니터링 스레드 시작
        self.start_monitoring()  
        self.setFixedSize(600, 900)  # 고정된 크기 설정


    # UI 요소 생성
    def create_ui_elements(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 기존에 생성된 User_label QLabel 위젯 가져오기
        self.User_label = self.ui.Label_User_Text
        self.User_label.setWordWrap(True)  # 텍스트 자동 줄 바꿈 활성화

        # 기존에 생성된 Model_label QLabel 위젯 가져오기
        self.Model_label = self.ui.Label_Model_Text
        self.Model_label.setWordWrap(True)  # 텍스트 자동 줄 바꿈 활성화

         # 콤보박스 선택 시그널 연결
        self.ui.cbox_Model.currentIndexChanged.connect(self.handle_model_selection)

    def update_image(self, image):
        # 이미지 라벨 업데이트
        self.ui.Cam_window.setPixmap(QPixmap.fromImage(image))

    # 마이크 버튼 클릭 이벤트 핸들러
    def toggle_mike(self):
        self.mike_on = not self.mike_on  # 마이크 상태 변경
        self.update_mike_button()  # 마이크 버튼 텍스트 업데이트 요청

    # 마이크 스레드 시작, 입력 받아 텍스트 추출
    def start_mike_thread(self):
        self.mike_thread = Mike_thread2()
        self.mike_thread.result_text.connect(self.update_user_txt)
        self.mike_thread.start()

    # 마이크 종료 및 재시작
    def stop_mike_thread(self):
        if self.mike_thread is not None and self.mike_thread.isRunning():
            self.mike_thread.stop() 
            self.mike_thread.finished.connect(self.mike_thread_finished)  
            self.mike_thread.start() 

    def mike_thread_finished(self):
        self.mike_thread.wait() 
        print("마이크가 종료되었습니다.")

    def on_mike_button_clicked(self):
        if not self.mike_status:
            self.start_mike_thread()
            self.mike_status = True
            self.ui.btn_Mike_on.setText("Stop Mike")
        else:
            self.stop_mike_thread()
            self.mike_status = False
            self.ui.btn_Mike_on.setText("Start Mike")
 

    def update_user_txt(self, text):
        # 텍스트 출력
        if text:
            print(text)
            # 마이크에서 받은 텍스트를 UI 상의 Label에 설정
            self.User_label.setText(text)

            # UI 업데이트 요청을 보냅니다.
            self.signals.userTextChanged.emit(text)


    # 모델 구성 업데이트 스레드 시작
    def start_model_config_thread(self):
        self.model_config_thread = ModelConfigThread(self.model_configs, self.assistant)
        self.model_config_thread.start()

     # 모니터링 스레드 시작
    def start_monitoring(self):
        self.file_monitor = FileMonitor(self.data_path, self.process_audio, model_index=0, ui_signal=self.signals.mike_off)
        self.signals.userTextChanged.connect(self.process_user_text)
        self.file_monitor.start()

    def handle_model_selection(self):
    # 콤보박스에서 선택된 텍스트에 따라 모델 설정
        selected_text = self.ui.cbox_Model.currentText()
        model_index_map = {"F": 0, "T": 1, "Default": 2}
        selected_index = model_index_map.get(selected_text)
        if selected_index is not None:
            self.selected_model_index = selected_index  # 선택된 모델 인덱스 업데이트
            selected_model_config = self.model_configs[self.selected_model_index]
            self.assistant.update_model_config(selected_model_config)  # 모델 구성 업데이트
            print("현재 선택된 모델:", selected_text)


    # 오디오 처리 콜백 함수
    def process_audio(self, file_path, model_index):
    # AudioTranscriber 인스턴스 생성
        transcriber = AudioTranscriber(file_path)
        # transcribe_audio 메서드 호출하여 transcript 값을 받아옴
        transcript = transcriber.transcribe_audio()
       # 텍스트 출력
        if transcript:
            self.User_label.setText(transcript)  # User_label의 텍스트를 transcript로 설정
            user_text = self.User_label.text()
            self.signals.userTextChanged.emit(user_text)  # Emit userTextChanged signal with the updated text


          # 사용자의 텍스트를 User_label에서 가져옵니다.
        user_text = self.User_label.text()
            
        # 파일 삭제
        os.remove(file_path)
        # UI 업데이트 요청을 보냅니다.
        self.signals.mike_off.emit()


    def process_user_text(self, user_text):
        # 처리할 텍스트가 있는지 확인합니다.
        if user_text:
            # ChatGPTAssistant를 사용하여 사용자 텍스트를 기반으로 응답을 생성합니다.
            response = self.assistant.chat_with_gpt(user_text, self.selected_model_index)
                
        # 생성된 응답을 Model_label에 업데이트합니다.
        if response:
            self.Model_label.setText(response)

    def voice_button_clicked(self):
        # Model_label에서 텍스트 가져오기
        model_txt = self.Model_label.text()

        # gTTS를 사용하여 텍스트를 음성으로 변환
        tts = gTTS(text=model_txt, lang='ko')
        
        # 재생할 음성 파일 생성
        tts_path = 'output.mp3'
        tts.save(tts_path)

        # 음성 파일 재생
        pygame.mixer.init()
        pygame.mixer.music.load(tts_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        os.remove(tts_path)

     # 윈도우가 닫힐 때 호출되는 이벤트 핸들러
    def closeEvent(self, event):
        # 각 스레드 중지
        if self.webcam_thread.isRunning():
            self.webcam_thread.terminate()  # 웹캠 스레드 종료
            self.webcam_thread.wait()  # 종료될 때까지 대기

        if self.mike_thread is not None and self.mike_thread.isRunning():
            self.mike_thread.stop()  # 마이크 스레드 종료 요청
            self.mike_thread.finished.connect(self.mike_thread_finished)  # 스레드가 종료될 때까지 대기

        #속성이나 메서드의 존재 여부를 확인
        if hasattr(self.model_config_thread, 'is_alive') and self.model_config_thread.is_alive():
            self.model_config_thread.stop()  # 모델 구성 업데이트 스레드 종료
        if self.file_monitor.running:
            self.file_monitor.stop()  # 모니터링 스레드 종료
        event.accept()  # GUI 종료

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ChatModule()
    window.show()
    app.exec_()
