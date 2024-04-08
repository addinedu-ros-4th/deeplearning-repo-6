import cv2
import cvlib as cv
import os
import yaml

class FaceRecognizer:
    def __init__(self, model_path, names_dict_path):
        self.recognizer = cv2.face.LBPHFaceRecognizer.create()
        self.recognizer.read(model_path)
        self.names_dict = self.load_names_dict(names_dict_path)

    def load_names_dict(self, names_dict_path):
        with open(names_dict_path, 'r', encoding='utf-8') as file:
            names_dict = yaml.safe_load(file)
        return names_dict

    def recognize_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces, confidences = cv.detect_face(frame)
        recognized_name = ""

        for face, confidence in zip(faces, confidences):
            startX, startY, endX, endY = face
            face_img_gray = gray[startY:endY, startX:endX]

            id, confidence = self.recognizer.predict(face_img_gray)
            
            if confidence >= 45 and confidence <= 100:
                name = list(self.names_dict.keys())[list(self.names_dict.values()).index(id)]
                recognized_name = name
                color = (0, 0, 255)  # 빨간색
            else:
                name = "Unknown"
                color = (255, 255, 255)  # 흰색
            
            confidence_str = "  {0}%".format(round(confidence))
            
            # cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            # cv2.putText(frame, name, (startX+5, startY-5), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            # cv2.putText(frame, confidence_str, (startX+5, endY-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 1)

        return frame, recognized_name

# if __name__ == "__main__":
#     current_path = os.getcwd()  # 현재 경로 가져오기
#     model_path = os.path.join(current_path, 'faces_trained.yaml')  # 현재 경로의 faces_trained.yaml로 경로 설정
#     names_dict_path = os.path.join(current_path, 'faces_trained_labels.yaml')  

#     face_recognizer = FaceRecognizer(model_path, names_dict_path)

#     cam = cv2.VideoCapture(0)
#     cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#     cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#     while True:
#         ret, frame = cam.read()

#         if not ret:
#             print("Failed to grab frame")
#             break

#         frame, recognized_name = face_recognizer.recognize_faces(frame)
#         print(recognized_name)

#         cv2.imshow('Camera', frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cam.release()