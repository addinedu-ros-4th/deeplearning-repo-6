
# 데이터베이스 테이블 생성 쿼리
CREATE TABLE IF NOT EXISTS Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    DOB DATE,
    Gender ENUM('남', '여', 'Other'),
    Password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS RobotSetting (
    SettingID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    Model ENUM('F', 'T', 'Thanos', 'Default') NOT NULL,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE IF NOT EXISTS LoginRecords (
    RecordID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    LoginTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users (UserID)
);

-- CREATE TABLE FaceRecData (
--     DataID INT AUTO_INCREMENT PRIMARY KEY,
--     UserID INT,
--     FaceData VARCHAR(255) NOT NULL,
--     FOREIGN KEY (UserID) REFERENCES Users(UserID)
-- );
