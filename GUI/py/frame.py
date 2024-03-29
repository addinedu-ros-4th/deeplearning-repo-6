import cv2
import os

def init_camera(video, name):
    save_folder = '/home/addinedu/git_ws/deeplearning-repo-6/GUI/data'

    if not video.isOpened():
        print("Video is unavailable :", video)
        exit(0)

    fps = video.get(cv2.CAP_PROP_FPS)
    count = 0

    while(video.isOpened()):
        ret, image = video.read()

        if not ret:
            print("Failed to grab frame")
            break

        # 프레임마다 이미지 저장
        frame_file_path = os.path.join(save_folder, "{}_frame_{}.jpg".format(name, count))

        # 프레임 저장
        cv2.imwrite(frame_file_path, image)
        count += 1

    video.release()
