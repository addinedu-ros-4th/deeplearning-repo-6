import os
import cv2
import numpy as np

# LBPH 얼굴 인식기 생성
recognizer = cv2.face.LBPHFaceRecognizer_create()

# 저장된 이미지 경로
image_folder = '/home/jongchanjang/amr_ws/opencv_study/source/images/'

print("학습 중")

# 저장된 이미지를 로드하고 얼굴 영역 추출하여 학습 데이터 생성
def prepare_training_data(folder_path):
    # 이미지 파일 경로 가져오기
    image_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if not f.startswith('.front') and f.endswith(('.jpg', '.jpeg', '.png'))]
    
    faces = []
    labels = []

    for image_path in image_paths:
        # 이미지 로드 (흑백으로)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # 이미지 리스트에 추가
        faces.append(image)

        # 라벨 리스트에 추가
        label = os.path.splitext(os.path.basename(image_path))[0].split(".")[1].split(".")[0]  # 파일 이름에서 확장자 제거
        labels.append(int(label))

    return faces, labels

# 학습 데이터 준비
faces, labels = prepare_training_data(image_folder)

# 학습 데이터를 사용하여 얼굴 인식 모델 학습
recognizer.train(faces, np.array(labels))

print("학습된 얼굴 라벨 갯수 :", len(set(labels)))

# 학습된 모델 저장
recognizer.save('/home/jongchanjang/amr_ws/opencv_study/source/trained_model.yaml')

print("학습 완료")