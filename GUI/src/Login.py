import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIntValidator

class LoginWindow(QMainWindow):
    def __init__(self,main_window):
        super().__init__()
        # UI 파일 로드
        self.main_window = main_window     
        self.resize(476,470)

        self.ui = loadUi('GUI/ui/Login.ui', self)
        # 버튼 클릭 이벤트 핸들러 연결
        self.Btn_Login.clicked.connect(self.login_clicked)

        # 비밀번호 입력 상자의 기본값 비우기
        self.ui.Txt_Pw.clear()

        # 비밀번호 입력 상자에 숫자 4자리 제한 설정
        self.ui.Txt_Pw.setValidator(QIntValidator(0, 9999))

    def login_clicked(self):
        # 로그인 버튼 클릭 시 수행할 작업 정의
        # 예시로 당신의 이름과 비밀번호를 출력하는 작업 수행
        name = self.ui.Txt_Name.toPlainText()
        password = self.ui.Txt_Pw.text()
        print("이름:", name)
        print("비밀번호:", password)
        if len(password) < 4:
            QMessageBox.warning(self, "경고", "비밀번호는 4자리만 가능합니다.")
        elif name == "최가은" and password == "1234":
            self.main_window.show_Sr_page()  # MainWindow 객체의 show_Sr_page 메서드 호출
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
