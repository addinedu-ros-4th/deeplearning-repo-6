import os
import cv2
import cvlib as cv

# 웹캠 열기
cam = cv2.VideoCapture(0)

# 저장할 얼굴 이미지의 수
image_count = 0

# 얼굴 클래스 설정 (1부터 / 저장된 id 확인 후 그 다음부터!)
user_id = input("사용자 id를 입력하세요: ")

while True:
    ret, frame = cam.read()  # 비디오 프레임 읽기
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 그레이스케일 변환
    
    # 얼굴 찾기
    faces, confidences = cv.detect_face(frame)

    for (x, y, x2, y2), conf in zip(faces, confidences):

        # 감지된 얼굴 영역을 잘라내서 저장
        face_img = frame[y:y2, x:x2]  # 얼굴 영역을 잘라냄

        image_count += 1

        # 얼굴을 이미지 파일로 저장
        file_path = "/home/jongchanjang/amr_ws/opencv_study/source/images/USER.{}.{}.jpg".format(user_id, image_count)
        cv2.imwrite(file_path, face_img) 

        # 얼굴위치 bbox 그리기
        cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)

        # 이미지 개수를 얼굴 영역 위에 표시
        cv2.putText(frame, str(image_count), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # 영상 출력
    cv2.imshow('image', frame)

    if image_count == 100:# 100장 저장 후 멈추고 엔터 대기
        input("앞면 100장 저장되었습니다. 엔터를 누르면 왼쪽 옆면 100장을 저장합니다.")
    
    if image_count == 200:# 200장 저장 후 멈추고 엔터 대기
        input("왼쪽 옆면 100장 저장되었습니다. 엔터를 누르면 오른쪽 옆면 100장을 저장합니다.")

    if image_count == 300:# 300장 저장 후 멈추고 엔터 대기
        input("오른쪽 옆면 100장 저장되었습니다. 엔터를 누르면 밑면 100장을 저장합니다.")

    if image_count == 400:# 400장 저장 후 멈추고 엔터 대기
        input("밑면 100장 저장되었습니다. 엔터를 누르면 윗면 100장을 저장합니다.")

    key = cv2.waitKey(1)
    if key == ord('q') or image_count >= 500:  # 'q' 키를 누르거나 500장 이상 저장되면 종료
        input("윗면 500장 저장되었습니다. 엔터를 누르면 종료가 됩니다.")
        break

cam.release()
cv2.destroyAllWindows()