import speech_recognition as sr
import Mike as mk

#import sys #-- 텍스트 저장시 사용
class Speech_recognizer:
    def __init__(self) -> None:
        self.audio_path = ""
        self.recognizer = sr.Recognizer()
        self.text = ""

    def recognition(self,audio):
        text = self.recognizer.recognize_google(audio, language='ko-KR')
        self.text = text

    def get_text(self):
        return self.text
    

"""

r = sr.Recognizer()
kr_audio = sr.AudioFile('/home/djy0404/amr_ws/project/communication_model/test_audio/news.wav')

with kr_audio as source:
    audio = r.record(source)
    #sys.stdout = open('news_out.txt', 'w') #-- 텍스트 저장시 사용

text = r.recognize_google(audio, language='ko-KR')
print(f"변환된 문자 : {text}") #-- 한글 언어 사용

"""
vr =mk.VoiceRecorder()
vr.start_recording()
vr.save_recording()
r = sr.Recognizer()
kr_audio = sr.AudioFile("/home/djy0404/amr_ws/project/communication_model/record/output.wav")

with kr_audio as source:
    audio = r.record(source)
    #sys.stdout = open('news_out.txt', 'w') #-- 텍스트 저장시 사용

text = r.recognize_google(audio, language='ko-KR')
print(f"변환된 문자 : {text}") #-- 한글 언어 사용

# obtain audio from the microphone
"""r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    text = r.recognize_google(audio, language='ko-KR')
    print("Google Speech Recognition thinks you said " + text)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))"""