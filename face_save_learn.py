import os
import cv2
import numpy as np
import yaml
import cvlib as cv

class FaceImageCollectorAndRecognizerTrainer:
    def __init__(self, image_folder, model_save_path):
        self.image_folder = image_folder
        self.model_save_path = model_save_path
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.label_dict = {}  # 사용자 이름과 정수 라벨을 매핑하는 딕셔너리

    def collect_face_images(self, user_id):
        cam = cv2.VideoCapture(0)
        image_count = 0

        while True:
            ret, frame = cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces, confidences = cv.detect_face(frame)

            for (x, y, x2, y2), conf in zip(faces, confidences):
                face_img = frame[y:y2, x:x2]

                image_count += 1
                file_path = os.path.join(self.image_folder, f"USER.{user_id}.{image_count}.jpg")
                cv2.imwrite(file_path, face_img)

                cv2.rectangle(frame, (x, y), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, str(image_count), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            cv2.imshow('image', frame)

            if image_count == 100:
                input("100장 저장되었습니다. 엔터를 누르면 다음 단계로 넘어갑니다.")
            elif image_count == 200:
                input("200장 저장되었습니다. 엔터를 누르면 다음 단계로 넘어갑니다.")
            elif image_count == 300:
                input("300장 저장되었습니다. 엔터를 누르면 다음 단계로 넘어갑니다.")
            elif image_count == 400:
                input("400장 저장되었습니다. 엔터를 누르면 다음 단계로 넘어갑니다.")

            key = cv2.waitKey(1)
            if key == ord('q') or image_count >= 500:
                input("500장 저장되었습니다. 엔터를 누르면 종료됩니다.")
                break

        cam.release()
        cv2.destroyAllWindows()

    def prepare_training_data(self):
        image_paths = [os.path.join(self.image_folder, f) for f in os.listdir(self.image_folder) if not f.startswith('.front') and f.endswith(('.jpg', '.jpeg', '.png'))]
        faces = []
        labels = []

        for image_path in image_paths:
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            faces.append(image)
            user_name = os.path.splitext(os.path.basename(image_path))[0].split(".")[1].split(".")[0]
            
            # 이미 등록된 사용자인지 확인 후 라벨 부여
            if user_name not in self.label_dict:
                self.label_dict[user_name] = len(self.label_dict)  # 새로운 사용자일 경우 정수 라벨 부여
            label = self.label_dict[user_name]
            
            labels.append(label)

        return faces, labels

    def train_model(self):
        print("학습 중")
        faces, labels = self.prepare_training_data()
        self.recognizer.train(faces, np.array(labels))
        print("학습된 얼굴 라벨 갯수 :", len(set(labels)))
        self.recognizer.save(self.model_save_path)
        
        # 딕셔너리도 함께 저장
        with open(os.path.splitext(self.model_save_path)[0] + '_labels.yaml', 'w') as file:
            yaml.dump(self.label_dict, file, allow_unicode=True)

        print("학습 완료")

if __name__ == "__main__":
    user_id = input("사용자 이름을 입력하세요: ")
    image_folder = '/home/jongchanjang/amr_ws/opencv_study/source/faces/'
    model_save_path = '/home/jongchanjang/amr_ws/opencv_study/source/faces_trained.yaml'
    
    face_collector_and_trainer = FaceImageCollectorAndRecognizerTrainer(image_folder, model_save_path)
    face_collector_and_trainer.collect_face_images(user_id)
    face_collector_and_trainer.train_model()