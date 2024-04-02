# 데이터베이스 생성, 삽입, 버튼 연동
import mysql.connector
import pandas as pd

class DatabaseManager:
    def __init__(self, host, user):
        self.host = host
        self.user = user
        self.db_name = "tear"
        self.cur = None
        self.conn = None
    
    
    # 데이터베이스 연결
    def connect_database(self, db_name=None):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            database = db_name
            )
        self.cur = self.conn.cursor()
        
        # 데이터베이스가 없다면 생성
        self.create_database()
        
            
    # 데이터베이스 생성
    def create_database(self):
        self.execute_sql_file("/home/addinedu/git_ws/deeplearning-repo-6/DB/query/create_db.sql")
        self.cur.execute("USE tear")
        
    # 테이블 생성
    def create_table(self):
        self.execute_sql_file("/home/addinedu/git_ws/deeplearning-repo-6/DB/query/create_table.sql")
        
    
    # query 실행
    def execute_sql_file(self, file_path):
        with open(file_path, 'r') as file:
            sql_script = file.read()
            
        commands = sql_script.split(';')
        
        for command in commands:
            try:
                if command.strip() != '':
                    self.cur.execute(command)
            except mysql.connector.Error as err:
                print(f"Error occurred: {err}")
        
        self.conn.commit()
    
    
    # 데이터베이스에 사용자 정보 저장
    def save_data(self, name, gender, birth, password):
        if gender in ["남성", "남자", "Male", "남"]:
            gender = "남"
        elif gender in ["여성", "여자", "Female", "여"]:
            gender = "여"
        else:
            gender = "Other"
            
        query = "INSERT INTO Users (Name, Gender, DOB, Password) VALUES (%s, %s, %s, %s)"
        self.cur.execute(query, (name, gender, birth, password))
        self.conn.commit()

    
    def close_connection(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
    