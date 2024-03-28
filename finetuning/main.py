import os
import threading
from time import sleep
import signal
from mic_amp import AudioAmplifier
from mic import VoiceRecorder
from gpt import ChatGPTAssistant, ModelConfigThread
import time
import threading
from PyQt5 import QtWidgets
from PyQt5 import uic
from googleapi import FileMonitor, AudioTranscriber
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMainWindow, QApplication


Ui_MainWindow, QtBaseClass = uic.loadUiType("/home/ito/amr_ws/mechine learing/project/mic/gpt+stt/SR_gui.ui")

class Signal(QObject):
    mike_off = pyqtSignal()

class ChatModule(QtWidgets.QMainWindow):
    def __init__(self):
        super(ChatModule, self).__init__()

        # 데이터 경로 설정
        self.data_path = "/home/ito/amr_ws/mechine learing/project/mic/mic_data"

        # 모델 구성 정의
        self.model_configs = [
            {"model": "gpt-3.5-turbo", "system_message": "반말을 사용하고, 감정적이고 친화적인 경향을 가지며, 친근하고 상냥한 말투로 해줘.", "assistant_message": "좋은 하루 보내!"},
            {"model": "gpt-3.5-turbo", "system_message": "반말을 사용하고, 주로 논리적이고 분석적인 성향을 가지고 있으며, 객관적인 사고와 문제 해결에 뛰어나.", "assistant_message": "무슨 문제 있어?"},
            {"model": "gpt-3.5-turbo", "system_message": "딱딱한 말투를 사용하고, 자신이 저지른 악행에 대해 합리화를 잘할뿐더러 타인과 타협도 잘 하지 않는 완고한 성격이야", "assistant_message": "나는 필연적인 존재다."},
        ]

        # UI 요소 생성을 메인 스레드에서 수행
        self.create_ui_elements()

        # 마이크 상태 변경 시그널
        self.signals = Signal()

        # 마이크 버튼 클릭 이벤트 핸들러 연결
        self.ui.btn_Mike_on.clicked.connect(self.toggle_mike)

        # 마이크 상태 변수
        self.mike_on = False

        # 마이크 버튼 텍스트 업데이트
        self.update_mike_button()

        self.selected_model_index = 1  # 초기 모델 인덱스 설정
        
        # ChatGPTAssistant 인스턴스 생성
        self.assistant = ChatGPTAssistant(self.model_configs)
        
        # 모델 구성 업데이트 스레드 시작
        self.start_model_config_thread()
        
        # 모니터링 스레드 시작
        self.start_monitoring()  


    # UI 요소 생성
    def create_ui_elements(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 기존에 생성된 User_label QLabel 위젯 가져오기
        self.User_label = self.ui.User_label
        self.User_label.setWordWrap(True)  # 텍스트 자동 줄 바꿈 활성화

        # 기존에 생성된 Model_label QLabel 위젯 가져오기
        self.Model_label = self.ui.Model_label
        self.Model_label.setWordWrap(True)  # 텍스트 자동 줄 바꿈 활성화

         # 콤보박스 선택 시그널 연결
        self.ui.cbox_Model.currentIndexChanged.connect(self.handle_model_selection)

    # 마이크 버튼 클릭 이벤트 핸들러
    def toggle_mike(self):
        self.mike_on = not self.mike_on  # 마이크 상태 변경
        self.update_mike_button()  # 마이크 버튼 텍스트 업데이트 요청

    # 마이크 버튼 텍스트 업데이트
    def update_mike_button(self):
        if self.mike_on:
            self.ui.btn_Mike_on.setText("Mic On")
        else:
            self.ui.btn_Mike_on.setText("Mic Off")

    # 모델 구성 업데이트 스레드 시작
    def start_model_config_thread(self):
        self.model_config_thread = ModelConfigThread(self.model_configs, self.assistant)
        self.model_config_thread.start()


    # 모델 구성 업데이트 스레드 시작
    def start_model_config_thread(self):
        self.model_config_thread = ModelConfigThread(self.model_configs, self.assistant)
        self.model_config_thread.start()

     # 모니터링 스레드 시작
    def start_monitoring(self):
        self.file_monitor = FileMonitor(self.data_path, self.process_audio, model_index=0, ui_signal=self.signals.mike_off)
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

            # 모델에 따른 대답 생성
            response = self.assistant.chat_with_gpt(transcript, self.selected_model_index)
            if response:
                self.ui.Model_label.setText(response)  # Model_label의 텍스트를 생성된 대답으로 설정
         # 파일 삭제
        os.remove(file_path)
        # UI 업데이트 요청을 보냅니다.
        self.signals.mike_off.emit()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = ChatModule()
    window.show()
    app.exec_()