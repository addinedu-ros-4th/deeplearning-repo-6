# 데이터베이스 생성, 삽입, 버튼 연동
import mysql.connector
import pandas as pd

class DatabaseManager:
    def __init__(self, host, user):
        self.host = host
        self.user = user
        self.db_name = "tier"
        self.cur = None
        self.conn = None
    
    # 데이터베이스 연결
    def connect_database(self, db_name=None):
        if db_name is None:
            db_name = self.db_name
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                database=db_name,
            )
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user
                )
                self.cur = self.conn.cursor()
                self.create_database(db_name)
                self.conn.database = db_name
            else:
                raise
        self.cur = self.conn.cursor()
        
        
    # 데이터베이스 생성
    def create_database(self, db_name):
        try:
            self.cur.execute(f"CREATE DATABASE {db_name}")
        except mysql.connector.Error as err:
            print(f"Failed creating database: {err}")
            exit(1)
        print(f"Database {db_name} created successfully.")
        self.cur.execute(f"USE {db_name}")
        
        
    # 테이블 생성
    def create_table(self):
        self.execute_sql_file("DB/query/create_table.sql")
        
    
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
        query = "INSERT INTO Users (Name, Gender, DOB, Password) VALUES (%s, %s, %s, %s)"
        self.cur.execute(query, (name, gender, birth, password))
        self.conn.commit()

        query = "SELECT UserID FROM Users ORDER BY UserID DESC LIMIT 1;"
        self.cur.execute(query)
        user_id = self.cur.fetchone()[0]
        
        return user_id
    
    # 데이터베이스에 로봇 정보 저장
    def save_robot_setting(self, user_id, model):
        query = "INSERT INTO RobotSetting (UserID, Model) VALUES (%s, %s)"
        self.cur.execute(query, (user_id, model))
        self.conn.commit()

    
    def close_connection(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
    