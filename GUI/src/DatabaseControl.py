# 데이터베이스 생성, 삽입, 버튼 연동
import mysql.connector
import pandas as pd

class DatabaseManager:
    def __init__(self, host, user):
        self.host = host
        self.user = "root"
        self.db_name = "tier"
        self.cur = None
        self.conn = None
        self.password = "1234"
    
    # 데이터베이스 연결
    def connect_database(self, db_name=None):
        if db_name is None:
            db_name = self.db_name
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                database=db_name,
                password=self.password
            )
            
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.conn = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password
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

    # 최근 등록한 이름 가져오기 
    def get_last_user_name(self):
        query = "SELECT Name FROM Users ORDER BY UserID DESC LIMIT 1"
        self.cur.execute(query)
        result = self.cur.fetchone()
        if result:
            return result[0]
        else:
            return None

    def find_elements(self, name, password):
        query = "SELECT UserId, Name, Password from Users where Name = %s and (Password) = %s;"
        self.cur.execute(query, (name, password))
        result = self.cur.fetchone()
        self.close_connection()
        return result
    
    # 데이터베이스에 로그인 기록 저장
    def save_login_records(self, userID):
        if not self.conn.is_connected():  # 커넥션이 연결되어 있지 않으면
            self.connect_database()  # 데이터베이스에 연결
        query = "INSERT INTO LoginRecords (UserID) VALUES (%s)"
        self.cur.execute(query, (userID,))
        self.conn.commit()
    
    def find_username(self):
        query = " SELECT Name  FROM Users  WHERE UserID = (SELECT UserID FROM LoginRecords ORDER BY RecordID DESC LIMIT 1);"
        self.cur.execute(query)
        result = self.cur.fetchone()
        if result:
            username = result[0]
        else:
            username = None
        return username

    def find_usermodel(self):
        query = " SELECT Model FROM RobotSetting WHERE UserID = (SELECT UserID FROM LoginRecords ORDER BY RecordID DESC LIMIT 1);"
        self.cur.execute(query)
        result = self.cur.fetchone()
        if result:
            usermodel = result[0]
        else:
            usermodel = None
        return usermodel
    
    def update_usermodel(self, selected_text):
        query = "UPDATE RobotSetting SET Model = %s WHERE UserID = (SELECT UserID FROM LoginRecords ORDER BY RecordID DESC LIMIT 1);"
        self.cur.execute(query, (selected_text,))
        self.conn.commit()
        

    def close_connection(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
    
    
<<<<<<< Updated upstream
    
=======
    def find_elements(self, name, password):
        query = "SELECT UserId, Name, Password from Users where Name = %s and (Password) = %s;"
        self.cur.execute(query, (name, password))
        result = self.cur.fetchone()
        self.close_connection()
        return result is not None
>>>>>>> Stashed changes
