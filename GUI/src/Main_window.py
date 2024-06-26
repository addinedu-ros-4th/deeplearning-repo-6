import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from GUI.src.Login import LoginWindow
from GUI.src.SR import ChatModule
from GUI.src.userSetting import UserRegistrationForm
from GUI.src.inputUser import InputUserClass
from GUI.src.train import TrainClass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_page = uic.loadUi('GUI/ui/Main_window.ui')
        self.setWindowTitle("RobotFace")
        main_size = self.main_page.size()
        width = main_size.width()
        height = main_size.height()
        self.main_page.setFixedSize(width, height)  # width와 height는 원하는 크기입니다.

        self.stacked_widget = QStackedWidget(self)  # QStackedWidget 인스턴스 생성
        self.setCentralWidget(self.stacked_widget)  # MainWindow의 중앙 위젯으로 설정

        self.stacked_widget.addWidget(self.main_page)  # Main 페이지를 stacked widget에 추가

        self.stacked_widget.setCurrentWidget(self.main_page)  # 처음에 Main 페이지를 보여줌

        self.main_page.Btn_Login.clicked.connect(self.show_login_page)  # 로그인 페이지로 전환
        self.main_page.Btn_regist.clicked.connect(self.show_regist_page)  # 사용자등록 페이지로 전환

        image_path = 'GUI/data/robot.png'
        self.show_image(image_path)

    
    def show_image(self, image_path):
        pixmap = QPixmap(image_path)  # 이미지 파일을 QPixmap으로 변환합니다.
        pixmap = pixmap.scaled(self.main_page.Label_Image.size(), aspectRatioMode=False)
        self.main_page.Label_Image.setPixmap(pixmap)  # QLabel에 이미지를 설정합니다.
    
    
    def show_login_page(self):
        self.login_page = LoginWindow(self)
        self.stacked_widget.addWidget(self.login_page)  # Login 페이지를 stacked widget에 추가
        self.stacked_widget.setCurrentWidget(self.login_page)  # Login 페이지를 보여줌


    def show_Sr_page(self):
        self.Sr_page = ChatModule(self) 
        self.stacked_widget.addWidget(self.Sr_page) #SR 페이지를 stacked widget에 추가
        self.stacked_widget.setCurrentWidget(self.Sr_page)

    def show_regist_page(self):
        self.user_setting_page = UserRegistrationForm(self) 
        self.stacked_widget.addWidget(self.user_setting_page) #SR 페이지를 stacked widget에 추가
        self.stacked_widget.setCurrentWidget(self.user_setting_page)


    def show_inputUser_page(self):
        self.inputUser_page = InputUserClass(self) 
        self.stacked_widget.addWidget(self.inputUser_page) #SR 페이지를 stacked widget에 추가
        self.stacked_widget.setCurrentWidget(self.inputUser_page)
    
    def show_train_page(self):
        self.train_page = TrainClass(self)
        self.stacked_widget.addWidget(self.train_page)
        self.stacked_widget.setCurrentWidget(self.train_page)


    def show_main_page(self):
        self.stacked_widget.setCurrentWidget(self.main_page)

    def closeEvent(self, event):
        if hasattr(self.Sr_page, 'closeEvent'):
            self.Sr_page.closeEvent(event)
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())