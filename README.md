## 음성 인식과 객체 인식을 기반으로 한 대화형 모델
> 팀명 : ```티어✨``` \
> ```티어```는 실버를 넘어 골드, 다이아를 모두 포함합니다. <br>
> '앞으로의 더 빛날 미래를 응원한다'는 의미를 담고 있습니다.
![Tier_Logo_Title](https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/c4c3d6b3-b8cf-41b0-99a1-9cd5e4f3413f)

<br>

## 💬 프로젝트 목적
1인 가구가 늘고 있는 현대 사회의 다양한 사람들의 고립감과 불편함을 해소하기 위해, 음성인식과 객체인식 기술을 통합한 **대화형 반려로봇**을 개발하는 프로젝트를 제안합니다. \
<br>
이 반려로봇은 사용자의 음성을 인식하고, 개인을 식별하여 ```맞춤형 상호작용```을 제공합니다. <br>
<br>
이 프로젝트의 목표는 외로움을 느끼는 사람들의 삶의 질을 향상시키고, **사회적 고립감**을 줄이는 것입니다.
<br><br>
### ❓맞춤형 상호작용이란
![Screenshot from 2024-04-08 15-45-26](https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/36732101-352c-4d08-879f-a107bfcc9adb)
<br>
<br>
MBTI ```F```와 ```T```의 답변은 매우 다릅니다. <br>
### 본인과 비슷한 성향의 로봇과 대화 하고 싶지 않나요? <br>
#### 그러기 위해 ***```개인화```*** 된 로봇에 초점을 맞추어 사용자를 ```인식```하고, ```맞춤형 대화```를 생성하는 모델을 개발하였습니다. <br>


<br>
<br>

##  📘 기술적 목표
1. **얼굴 인식** 기술을 활용하여 다양한 환경, 정확도 향상에 초점
2. **STT (Speech To Text)** 를 통해 마이크의 음성을 텍스트로 변환
3. **'Chat GPT' Fine Turning**을 통해 사용자 맞춤형 모델을 학습하고, 적용
4. **TTS (Text To Speech)** 를 통해 텍스트를 음성 파일로 변환하고 출력
5. **GUI**를 통해 사용자 정보를 받고, 얼굴 정보 실시간 학습
<br>

## 🔄 구동 프로세스
![구동 프로세스](https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/9c582500-abe4-4bdc-9b7f-32059f38329f)

<br>

## 👦 얼굴 인식 Sequence
![face_recognize_sequence](https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/a34d489c-86b0-437e-8389-eb341525d689)
<br>
<br>
## 🗣️ 음성 인식 Sequence
![Screenshot from 2024-04-11 19-35-43](https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/1e42b003-f39c-446e-89cc-e2dbaeac3cc8)





## 🤹 팀 구성원
| 도준엽 👑 | 최가은 | 장종찬 | 양혜경 | 임대환 |
| :-----------------: | :--------: | :--------: | :-------: | :-------: |
| <img src="https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/fb00f213-743f-462f-947d-1475f5ee963d" width="170"> | <img src="https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/62df3088-628b-4551-8ac3-9b3a2009c390" width="160">  | <img src="https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/5cf07b7c-ce29-4de7-a6fd-2bca61eeeb0e" width="170"> | <img src="https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/bb0a0579-8c6d-4481-ac6a-893ba91d448d" width="170"> | <img src="https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/d23fbd7e-0a7c-4d3f-9c09-c0ea068df991" width="170">  |
| [DJ_Y](https://github.com/djy0404)            | [ Silver ](https://https://github.com/gaeun0123)   | [Chan](https://github.com/jongchanjang)   | [HG_Y](https://github.com/hyegyeong-Y)  | [Hawn](https://github.com/Hwan9794)  |


<br>

## 🫂 역할
|구분|이름|업무|
|:---:|:---:|:---|
|팀장|도준엽|- 음성인식 오픈 소스 자료 조사 및 테스트 <br> - 마이크 음성 입력 모듈 제작 <br> - Speech Recognize 응용 모듈 구현|
|팀원|최가은|- 객체 인식 CNN 모델 생성 <br> - 모델 성능 평가 <br> - Database 구축, 관리 및 Database Control 모듈 구현 <br>|
|팀원|장종찬|- 객체 인식, 객체추적 모델 조사 및 구현 <br> - 얼굴인식 모델 조사 및 구현 <br>|
|팀원|양혜경|- 음성 인식 API 자료 조사 및 테스트 <br> - Google.cloud API 응용 <br> - GPT(chatbot) 구현 및 Fine Tuning <br>|
|팀원|임대환|- 객체 인식 모델 조사 및 구현 <br> - DB Query 작성 <br>|

<br>

## 🔎 기능 리스트
![tier_기능리스트](https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/90e12d4b-3162-499b-892b-c4796a529352)

<br>

## 📱 GUI 구성도
![face_flow-GUI 구성도 (1)](https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/a5460814-0197-4bab-88fc-1c8a4386296e)

## 📹 시현 영상
### 1. 사용자 얼굴 데이터 수집 <br>

[crop_cam.webm](https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/409162b0-fb3d-4faf-85ee-c1e9ac9f06ed)

여러 각도의 촬영을 통해 얼굴인식의 정확도를 높인다.

### 2. 얼굴 인식 모델로 학습 <br>

[crop_train.webm](https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/33feb121-3cfd-45b0-bdeb-458c5873f929)

CVlib 얼굴 인식 모델을 활용하여 수집한 데이터를 학습한다.

### 3. Face Login <br>

[crop_login.webm](https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/bd67ccc2-de00-4649-85ae-a86268e0cd4e)

학습된 모델을 사용하여 사용자를 인식하면 Login (사용자의 로봇에 접근) 할 수 있다.

### 4. 음성 인식, 답변 출력 <br>

[Screencast from 04-17-2024 07:04:08 PM.webm](https://github.com/addinedu-ros-4th/deeplearning-repo-6/assets/102429136/78f6d158-e84b-4959-9e24-519d048a7d55)

사용자는 GUI에서 상시 자신이 지정한 Robot Model 유형을 변경할 수 있다.

<br>

> 빛나는 미래를 선물할, 당신만의 로봇 동반자 '티어'와 함께하세요
> 
<br>
