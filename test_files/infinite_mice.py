import sys
sys.path.append('/home/djy0404/amr_ws/project/communication_model/kospeech_latest/')

import numpy as np
import torch
from kospeech_latest.kospeech.vocabs.ksponspeech import KsponSpeechVocabulary
from kospeech_latest.kospeech.data.data_loader import SpectrogramDataset,AudioDataLoader
import sounddevice as sd
import numpy as np

class Talking:
    def __init__(self) -> None:
        self.model_path = "model_ds2.pt"
        self.model = torch.load(self.model_path)
        self.vocab_path = "/home/djy0404/amr_ws/project/communication_model/kospeech_latest/data/vocab/aihub_character_vocabs.csv"
        self.vocab = KsponSpeechVocabulary(self.vocab_path)
        self.samplerate = 16000
        self.duration = 5  # 음성 입력의 지속 시간 (초)
    
    
    def mice_processing(self):
        #마이크에서 실시간으로 음성 입력 받기
        print("마이크에서 입력받는 중입니다...")
        audio_data = sd.rec(int(self.samplerate * self.duration), samplerate=self.samplerate, channels=1, dtype="int16")
        sd.wait()

        # 음성 데이터를 SpectrogramDataset 형식으로 변환
        audio = np.array(audio_data).reshape(1, -1)
        audio_data = torch.from_numpy(audio)

        # 음성 데이터를 모델의 입력 형식에 맞게 전처리
        spec_transform = SpectrogramDataset.parse_audio(audio_data)
        spec_transform = torch.unsqueeze(spec_transform, 0)

        # 추론 수행
        with torch.no_grad():
            self.model.eval()
            output = self.model(spec_transform)

        # 추론 결과를 텍스트로 변환
        ids = output.max(-1)[1].squeeze(0)
        sentence = self.vocab.label_to_string(ids)
        print("추론 결과:", sentence)

def main():
    t = Talking()
    t.mice_processing()

if __name__ == "__main__":
    main()
