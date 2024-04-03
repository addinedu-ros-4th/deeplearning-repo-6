
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_page = uic.loadUi('GUI/ui/Main_window.ui')

        self.stacked_widget = QStackedWidget(self)  # QStackedWidget 인스턴스 생성
        self.setCentralWidget(self.stacked_widget)  # MainWindow의 중앙 위젯으로 설정

        self.stacked_widget.addWidget(self.main_page)  # Main 페이지를 stacked widget에 추가
        main_widget_size = self.size()
        self.resize(main_widget_size)

        self.stacked_widget.setCurrentWidget(self.main_page)  # 처음에 Main 페이지를 보여줌

        self.main_page.Btn_Login.clicked.connect(self.show_login_page)  # 로그인 페이지로 전환
        self.main_page.Btn_regist.clicked.connect(self.show_regist_page)  # 사용자등록 페이지로 전환
        
        
        image_path = 'GUI/data/robot.png'
        self.show_image(image_path)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())