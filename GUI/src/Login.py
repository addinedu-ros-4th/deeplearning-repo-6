import sys
import cv2
from PyQt5.QtCore import pyqtSignal, QThread, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIntValidator
from GUI.src.DatabaseControl import DatabaseManager
from PyQt5.QtGui import QImage, QPixmap
from Face_recognize.face_recognize import FaceRecognizer
from PyQt5.QtCore import Qt

class WebCamThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage, str)

    def __init__(self):
        super().__init__()
        self.stopped = False
        self.model_path = "Face_recognize/model/model.yaml"
        self.names_dict_path = "Face_recognize/model/labels.yaml"
        self.face_recognizer = FaceRecognizer(self.model_path, self.names_dict_path)

    def stop(self):
        self.stopped = True

    def run(self):
        cap = cv2.VideoCapture(0)

        while not self.stopped:
            ret, frame = cap.read()  # 웹캠에서 프레임 읽기
            if ret:
                frame, recognized_name = self.face_recognizer.recognize_faces(frame)
                # print(recognized_name)

                # OpenCV에서 읽은 이미지를 PyQt용 QImage으로 변환
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                
                # 이미지 변경 신호를 발생시켜 메인 스레드로 이미지 전달
                self.change_pixmap_signal.emit(qt_image , recognized_name)
            else:
                print("Login page : failed to receive frame")
                break

        cap.release()

class LoginWindow(QMainWindow):
    def __init__(self,main_window):
        super().__init__()
        # UI 파일 로드
        self.main_window = main_window     
        self.resize(476,470)

        self.ui = loadUi('GUI/ui/Login.ui', self)

        # 웹캠 시작 시 스레드 실행
        self.webcam_thread = WebCamThread()
        self.webcam_thread.change_pixmap_signal.connect(self.update_image)  # 이미지 업데이트 신호 연결
        self.webcam_thread.start()  # 웹캠 스레드 시작

        # 버튼 클릭 이벤트 핸들러 연결
        self.Btn_Login.clicked.connect(self.login_clicked)

        # Database search
        self.db_manager = DatabaseManager("localhost", "root")
        
        # 비밀번호 입력 상자의 기본값 비우기
        self.ui.Txt_Pw.clear()

        # 비밀번호 입력 상자에 숫자 4자리 제한 설정
        self.ui.Txt_Pw.setValidator(QIntValidator(0, 9999))

    
    def update_image(self, image, recognized_name):
        # 이미지 라벨 업데이트
        pixmap = QPixmap.fromImage(image)
        scaled_pixmap = pixmap.scaled(self.ui.Cam_window.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # 이미지를 중앙에 배치
        self.ui.Cam_window.setPixmap(scaled_pixmap)
        self.ui.Cam_window.setAlignment(Qt.AlignCenter)

        self.name = ""
        if not self.name :
            self.name = recognized_name

        # 사용자 이름 업데이트
        self.ui.Txt_Name.setText(self.name)


    def login_clicked(self):
        # 로그인 버튼 클릭 시 수행할 작업 정의
        # 예시로 당신의 이름과 비밀번호를 출력하는 작업 수행
        name = self.ui.Txt_Name.toPlainText()
        password = self.ui.Txt_Pw.text()
        print("이름:", name)
        print("비밀번호:", password)
        if len(password) < 4:
            QMessageBox.warning(self, "경고", "비밀번호는 4자리만 가능합니다.")
        else:
            self.loginSuccess(name, password)  # MainWindow 객체의 show_Sr_page 메서드 호출
            
    
    def loginSuccess(self, name, password):
        self.db_manager.connect_database()
        
        userInfo = self.db_manager.find_elements(name, password)
        
        if userInfo:
            # 로그인 기록 저장
            userID = userInfo[0]
            self.db_manager.save_login_records(userID)
            
            # 로그인 성공 페이지로 전환
            self.webcam_thread.stop()
            self.webcam_thread.wait()
            self.main_window.show_Sr_page()
        else:
            QMessageBox.warning(self, "로그인 실패", "사용자 이름 또는 비밀번호가 잘못되었습니다.")
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
