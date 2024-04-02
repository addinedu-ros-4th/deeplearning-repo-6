
# 데이터베이스 테이블 생성 쿼리
CREATE TABLE IF NOT EXISTS Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    DOB DATE,
    Gender ENUM('남', '여', 'Other'),
    Password VARCHAR(255) NOT NULL
);

-- CREATE TABLE FaceRecData (
--     DataID INT AUTO_INCREMENT PRIMARY KEY,
--     UserID INT,
--     FaceData VARCHAR(255) NOT NULL,
--     FOREIGN KEY (UserID) REFERENCES Users(UserID)
-- );

-- CREATE TABLE RobotSetting (
--     SettingID INT AUTO_INCREMENT PRIMARY KEY,
--     UserID INT,
--     Model ENUM('F', 'T', 'Default') NOT NULL,
--     FormalSpeech BOOLEAN NOT NULL,
--     FOREIGN KEY (UserID) REFERENCES Users(UserID)
-- );