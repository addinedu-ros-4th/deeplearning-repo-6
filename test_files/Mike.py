import pyaudio
import numpy as np
import wave
import struct


class Mike:
    def __init__(self) -> None:
        self.mike_on = False
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000  # 샘플링 주파수 (Hz)
        self.CHUNK = 2048  # 오디오 프레임 크기, n_fft 값과 같게 설정
        self.RECORD_SECONDS = 5  # 녹음할 시간(초)
        self.WAVE_OUTPUT_FILENAME = "output.wav"
        self.THRESHOLD_ENERGY = 50000
        self.audio = pyaudio.PyAudio()

    def change_mike_state(self):
        self.mike_on = not self.mike_on
        print(self.mike_on)

    def get_audio(self):
        return self.audio
    
    def on_mike(self):
        audio = self.get_audio()
        stream = audio.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)
        
        frame = []
        while True:
            data = stream.read(self.CHUNK)
            frame.append(data)
            # 바이너리 데이터를 숫자 배열로 변환
            samples = struct.unpack(f'{self.CHUNK}h', data)
            # 음성 신호의 에너지 계산
            energy = np.sum(np.square(samples)) / self.CHUNK
            print(f'Energy: {energy}')
            # 음성 활동 감지
            if energy > self.THRESHOLD_ENERGY:
                print("Voice activity detected!")
            else:
                print("Silence detected!")
                stream.stop_stream()
                stream.close()
                audio.terminate()
                break
        return frame
        
        

    def make_audio_file(self):
        frame = self.on_mike()
        audio = self.audio
        with wave.open(self.WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frame))


def main():
    m = Mike()
    m.change_mike_state()
    m.change_mike_state()


if __name__ == "__main__":
    main()