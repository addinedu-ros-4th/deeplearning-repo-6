# 사용자 정보 등록 UI

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from GUI.src.DatabaseControl import DatabaseManager #데이터베이스 관리 클래스

class UserRegistrationForm(QMainWindow):
    def __init__(self,parent = None):
        super().__init__(parent)
        # UI 파일 로드
        loadUi("GUI/ui/userSetting.ui", self)
        self.setWindowTitle("사용자 정보 입력")
        
        # 사용자 등록 버튼에 클릭 이벤트 핸들러 연결
        self.Btn_resist.clicked.connect(self.register_user)
        
        self.db_connect()      # Database 객체 생성


    def register_user(self):
        # 사용자가 입력한 정보 가져오기
        name = self.Txt_name.toPlainText()
        gender = self.Txt_gender.toPlainText()
        birth = self.Txt_birth.toPlainText()
        password = self.Txt_pw.toPlainText()
        
        # 입력된 정보가 모두 존재하는지 확인
        if name.strip() and gender.strip() and birth.strip() and password.strip():
            # 모든 필드에 값이 존재하는 경우에만 사용자 등록 수행
            self.DBManager.save_data(name, gender, birth, password)
            self.DBManager.close_connection()
            print("사용자 등록 완료")
            
        else:
            # 입력 필드 중 하나 이상이 비어있는 경우에는 알림 메시지 표시
            QMessageBox.critical(self, "오류", "모든 필드를 입력하세요.")

    
    def db_connect(self):
        self.DBManager = DatabaseManager("localhost", "root")   # manager 객체 생성
        self.DBManager.connect_database()
        self.DBManager.create_table()
        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserRegistrationForm()
    window.show()
    sys.exit(app.exec_())