# 사용자 정보 등록 UI
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from GUI.src.inputUser import InputUserClass
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDate 
from PyQt5.QtGui import QIntValidator

from GUI.src.DatabaseControl import DatabaseManager #데이터베이스 관리 클래스

# 전역 변수로 사용자 이름 저장
global global_user_name
global_user_name = ""

class UserRegistrationForm(QMainWindow):
    def __init__(self,main_window):
        super().__init__()
        self.main_window = main_window 

        # UI 파일 로드
        loadUi("GUI/ui/userSetting.ui", self)
        
        self.setWindowTitle("사용자 정보 입력")

        # 성별 입력 라디오 버튼
        self.setup_radio_buttons()

        # 사용자 등록 버튼에 클릭 이벤트 핸들러 연결
        self.Btn_resist.clicked.connect(self.register_user)
        
        self.db_connect()      # Database 객체 생성

        # 현재 날짜를 가져와 dateEdit 위젯에 설정
        today = QDate.currentDate()
        self.dateEdit.setDate(today)
        
        # 비밀번호에 숫자 4자리 제한 설정
        self.Txt_pw.setValidator(QIntValidator(0, 9999))
        

    def setup_radio_buttons(self):
        # '남성' 라디오 버튼을 선택되어 있도록 설정
        self.radio_man.setChecked(True)
        
        # 라디오 버튼들이 하나만 선택되도록 설정
        self.radio_man.toggled.connect(lambda: self.on_radio_toggled(self.radio_man))
        self.radio_other.toggled.connect(lambda: self.on_radio_toggled(self.radio_other))
        self.radio_woman.toggled.connect(lambda: self.on_radio_toggled(self.radio_woman))

    def on_radio_toggled(self, clicked_radio):
        if clicked_radio.isChecked():
            for radio in [self.radio_man, self.radio_other, self.radio_woman]:
                if radio != clicked_radio:
                    radio.setChecked(False)

    def register_user(self):
        # 사용자가 입력한 정보 가져오기
        name = self.Txt_name.text() 
        password = self.Txt_pw.text()
        birth = self.dateEdit.date().toString("yyyy-MM-dd")  
        if self.radio_man.isChecked():
            gender = self.radio_man.text()
        elif self.radio_other.isChecked():
            gender = self.radio_other.text()
        elif self.radio_woman.isChecked():
            gender = self.radio_woman.text()

        # 입력된 정보가 모두 존재하는지 확인
        if name.strip() and gender.strip() and birth.strip() and password.strip():
            # 모든 필드에 값이 존재하는 경우에만 사용자 등록 수행
            self.DBManager.save_data(name, gender, birth, password)
            self.DBManager.close_connection()
            global_user_name = name # 이름을 전역변수에 입력
            # 화면 전환
            self.main_window.show_inputUser_page()
        else:
            # 입력 필드 중 하나 이상이 비어 있거나 비밀번호가 4자리가 아닌 경우 알림 메시지 표시
            QMessageBox.critical(self, "오류", "모든 필드를 입력하고 비밀번호는 4자리여야 합니다.")

    
    def db_connect(self):
        self.DBManager = DatabaseManager("localhost", "root")   # manager 객체 생성
        self.DBManager.connect_database()
        self.DBManager.create_table()
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserRegistrationForm()
    window.show()
    sys.exit(app.exec_())