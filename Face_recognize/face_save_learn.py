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

    # 데이터 준비 (얼굴)
    def prepare_training_data(self):
        faces = []
        labels = []

        for root, dirs, files in os.walk(self.image_folder):
            for dir_name in dirs:
                user_folder = os.path.join(self.image_folder, dir_name)
                image_paths = [os.path.join(user_folder, f) for f in os.listdir(user_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

                for image_path in image_paths:
                    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                    faces.append(image)
                    user_name = dir_name

                    # 이미 등록된 사용자인지 확인 후 라벨 부여
                    if user_name not in self.label_dict:
                        self.label_dict[user_name] = len(self.label_dict)  # 새로운 사용자일 경우 정수 라벨 부여
                    label = self.label_dict[user_name]

                    labels.append(label)

        return faces, labels


    # 사용자 얼굴 학습
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


    def check_training_success(self):
        model_path = os.path.splitext(self.model_save_path)[0] + '_labels.yaml'
        
        # 모델 파일 및 라벨 파일이 모두 존재하는지 확인
        if os.path.exists(self.model_save_path) and os.path.exists(model_path):
            # 모델 파일이 정상적으로 읽어지는지 확인
            try:
                self.recognizer.read(self.model_save_path)
            except Exception as e:
                print(f"Error loading model: {e}")
                return False
            
            # 라벨 파일이 정상적으로 읽어지는지 확인
            try:
                with open(model_path, 'r', encoding='utf-8') as file:
                    self.label_dict = yaml.safe_load(file)
            except Exception as e:
                print(f"Error loading label file: {e}")
                return False
            
            return True
        else:
            print("모델 또는 이름 파일이 존재 하지 않습니다!")
            return False
