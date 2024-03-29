import cv2
import cvlib as cv

# LBPH 얼굴 인식기 생성
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/jongchanjang/amr_ws/opencv_study/source/trained_model.yaml')

font = cv2.FONT_HERSHEY_SIMPLEX

# 사용자 id 번호 ! - 처음 사진 등록시 입력한 id가 이름 순서 ! 1번부터
names = ['None', 'jongchan' , 'junheck' , 'hyegyeong' , 'daehwan' , 'gauen' ]


# 웹캠 초기화
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

minW = 0.1 * cam.get(cv2.CAP_PROP_FRAME_WIDTH)
minH = 0.1 * cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

while True:
    ret, frame = cam.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 얼굴 감지
    faces, confidences = cv.detect_face(frame)

    if len(faces) == 0 :
        cv2.imshow('camera', frame)

    for face, confidence in zip(faces, confidences):
        startX, startY, endX, endY = face  # 얼굴 좌표
        face_img_gray = gray[startY:endY, startX:endX]  # 얼굴 영역의 그레이스케일 이미지

        # 얼굴 인식
        id, confidence = recognizer.predict(face_img_gray)

        if confidence >= 55 and confidence <= 100:
            id = names[id]
            color = (0, 0, 255)  # 빨간색
        else:
            id = "unknown"
            color = (255, 255, 255)  # 흰색
        
        confidence_str = "  {0}%".format(round(confidence))
        
        # 얼굴 주변에 박스 그리기
        cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

        # 얼굴 인식 결과와 신뢰도 출력
        cv2.putText(frame, id, (startX+5, startY-5), font, 1, color, 2)
        cv2.putText(frame, confidence_str, (startX+5, endY-5), font, 1, (255, 255, 0), 1)

    # 화면에 영상 표시
    cv2.imshow('camera', frame)

    # 'q'를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cam.release()
cv2.destroyAllWindows()