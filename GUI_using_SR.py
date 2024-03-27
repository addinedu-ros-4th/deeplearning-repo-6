import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.uic import loadUi
import speech_recognition as sr


class Mike_thread(QThread):
    result_text = pyqtSignal(str)
    finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.running = True  # 마이크 상태를 나타내는 변수
        
    def stop(self):
        self.running = False  # 마이크를 중지함
        
    def run(self):
        recognizer = sr.Recognizer()

        # 마이크 입력
        with sr.Microphone() as source:
            print("마이크로부터 입력을 받습니다...")
            while self.running:  # 마이크가 켜져 있는 동안 반복
                try:
                    # Google Web API를 이용하여 음성을 텍스트로 변환
                    audio_data = recognizer.listen(source, timeout=5)  # 5초 동안 입력을 대기
                    text = recognizer.recognize_google(audio_data, language="ko-KR")
                    self.result_text.emit(text)
                except sr.UnknownValueError:
                    print("음성을 이해할 수 없습니다.")
                except sr.RequestError as e:
                    print("Google Web API 요청이 실패했습니다. 에러 메시지:", e)
                if not self.running:
                    break
        self.finished.emit()  # 스레드 종료 시그널 발생


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        loadUi("/home/djy0404/amr_ws/project/communication_model/test_files/SR_gui.ui", self)  # UI 파일의 경로를 적절히 수정하세요
        self.mike_status = False
        self.mike_thread = None
        # 버튼 클릭 이벤트에 대한 핸들러 연결
        self.btn_Mike_on.clicked.connect(self.on_mike_button_clicked)
        self.btn_Output.clicked.connect(self.on_output_button_clicked)

    def start_mike_thread(self):
        self.mike_thread = Mike_thread()
        self.mike_thread.result_text.connect(self.update_user_txt)
        self.mike_thread.start()

    def stop_mike_thread(self):
        if self.mike_thread is not None and self.mike_thread.isRunning():
            self.mike_thread.stop()  # 마이크 스레드 중지
            self.mike_thread.finished.connect(self.mike_thread_finished)  # 스레드 종료 시그널 연결
            self.mike_thread.start()  # 마이크 스레드 재시작

    def mike_thread_finished(self):
        self.mike_thread.wait()  # 마이크 스레드가 종료될 때까지 대기
        print("마이크가 종료되었습니다.")

    def on_mike_button_clicked(self):
        if not self.mike_status:
            self.start_mike_thread()
            self.mike_status = True
            self.btn_Mike_on.setText("Stop Mike")
        else:
            self.stop_mike_thread()
            self.mike_status = False
            self.btn_Mike_on.setText("Start Mike")

    def update_user_txt(self, text):
        self.txt_User.setText(text)

    def on_output_button_clicked(self):
        print("음성 출력 버튼이 클릭되었습니다.")
        # 여기에 음성을 출력하는 코드를 추가하세요.


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
