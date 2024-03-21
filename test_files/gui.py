import sys
from PyQt5 import QtCore

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
import cv2

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 창의 타이틀 설정
        self.setWindowTitle("웹캠 및 음성 인식 GUI")

        # 웹캠을 통해 입력받은 화면을 출력할 레이블 생성
        self.webcam_label = QLabel(self)
        self.webcam_label.setFixedSize(640, 480)

        # 마이크 온/오프 버튼 생성
        self.microphone_button = QPushButton('마이크 ON', self)
        self.microphone_button.clicked.connect(self.toggle_microphone)

        # GPT 모드 선택 라벨 및 버튼 생성
        self.gpt_mode_label = QLabel('GPT 모드: ', self)
        self.gpt_mode_button_true = QPushButton('T', self)
        self.gpt_mode_button_false = QPushButton('F', self)
        self.gpt_mode_button_default = QPushButton('Default', self)
        self.gpt_mode_button_true.clicked.connect(lambda: self.set_gpt_mode(True))
        self.gpt_mode_button_false.clicked.connect(lambda: self.set_gpt_mode(False))
        self.gpt_mode_button_default.clicked.connect(lambda: self.set_gpt_mode(None))

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.webcam_label)
        layout.addWidget(self.microphone_button)
        layout.addWidget(self.gpt_mode_label)
        layout.addWidget(self.gpt_mode_button_true)
        layout.addWidget(self.gpt_mode_button_false)
        layout.addWidget(self.gpt_mode_button_default)

        # 윈도우에 레이아웃 설정
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # 웹캠 시작
        self.capture = cv2.VideoCapture(0)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # 초기 GPT 모드 설정
        self.gpt_mode = None

    def update_frame(self):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_qt_format)
            self.webcam_label.setPixmap(pixmap)

    def toggle_microphone(self):
        if self.microphone_button.text() == '마이크 ON':
            self.microphone_button.setText('마이크 OFF')
            # 마이크를 활성화하는 코드 추가
        else:
            self.microphone_button.setText('마이크 ON')
            # 마이크를 비활성화하는 코드 추가

    def set_gpt_mode(self, mode):
        if mode:
            self.gpt_mode = mode
            self.gpt_mode_label.setText(f'GPT 모드: {mode}')
        elif mode is False:
            self.gpt_mode = mode
            self.gpt_mode_label.setText(f'GPT 모드: {mode}')
        else:
            self.gpt_mode = None
            self.gpt_mode_label.setText(f'GPT 모드: Default')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
