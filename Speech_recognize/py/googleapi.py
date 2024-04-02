import os
import time
import threading
from google.cloud import speech_v1p1beta1 as speech
from PyQt5.QtCore import pyqtSignal, QObject, QThread

class Signal(QObject):
    mike_off = pyqtSignal()

class FileMonitor(threading.Thread):
    def __init__(self, data_path, callback, model_index, ui_signal):
        super().__init__()
        self.data_path = data_path
        self.callback = callback
        self.model_index = model_index
        self.ui_signal = ui_signal
        self.running = True
        self.processed_files = set()
    
    def run(self):
        while self.running:
            wav_files = [file for file in os.listdir(self.data_path) if file.endswith(".wav")]
            wav_files.sort(key=lambda x: int(os.path.splitext(x)[0]))
            
            for file in wav_files:
                if file not in self.processed_files:
                    file_path = os.path.join(self.data_path, file)
                    self.callback(file_path, self.model_index)
                    self.processed_files.add(file)  # 처리된 파일을 processed_files에 추가

            # 대기 중인 파일 제거
            for file in self.processed_files.copy():
                if file not in wav_files:
                    self.processed_files.remove(file)

            if len(self.processed_files) == len(wav_files):
                print("대기 중...")
                self.processed_files.clear()

            time.sleep(1)

    def stop(self):
        self.running = False

class AudioTranscriber:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def transcribe_audio(self):
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/djy0404/amr_ws/project/communication_model/test_files/GUI/google_key.json"
            client = speech.SpeechClient()

            with open(self.audio_file, "rb") as audio_file:
                content = audio_file.read()

            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
                language_code="ko-KR",
            )

            response = client.recognize(config=config, audio=audio)

            transcript = ""
            for result in response.results:
                best_alternative = result.alternatives[0]
                transcript += best_alternative.transcript + " "

            return transcript.strip()
        except Exception as e:
            print("Exception in AudioTranscriber:", str(e))
            return None