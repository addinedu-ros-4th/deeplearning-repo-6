import pyaudio
import struct
import numpy as np
import wave
import signal

# 마이크에서 음성을 받아들이는 파라미터 설정
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # 샘플링 레이트 (Hz)
CHUNK = 1024  # 버퍼 사이즈

# 에너지 기반 음성 활동 감지 임계값 설정
THRESHOLD_ENERGY = 10

# 마이크 스트림 열기
audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Listening...")

# 녹음 시작 시간 기록

# Ctrl+C 핸들링 함수
def signal_handler(sig, frame):
    # 마이크 스트림 닫기
    stream.stop_stream()
    stream.close()  
    audio.terminate()

    # 녹음된 음성 데이터 반환
    # 녹음된 음성을 WAV 파일로 저장
    output_wav_path = "recorded_audio.wav"
    with wave.open(output_wav_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Recorded audio saved at: {output_wav_path}")
    exit(0)

# Ctrl+C 시그널 핸들러 등록
signal.signal(signal.SIGINT, signal_handler)

# 에너지 기반 VAD 알고리즘 적용
frames = []
try:
    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        # 바이너리 데이터를 숫자 배열로 변환
        samples = struct.unpack(f'{CHUNK}h', data)
        # 음성 신호의 에너지 계산
        energy = np.sum(np.square(samples)) / CHUNK
        print(f'Energy: {energy}')
        # 음성 활동 감지
        if energy >= THRESHOLD_ENERGY:
            print("Voice activity detected!")
        else:
            stream.stop_stream()
            stream.close()  
            audio.terminate()
except KeyboardInterrupt:
    pass
finally:
    signal_handler(None, None)
