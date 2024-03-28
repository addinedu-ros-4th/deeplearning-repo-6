import pyaudio
import struct
import numpy as np
import wave
import signal
import time
import os

class VoiceRecorder:
    def __init__(self, threshold_energy=10):
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.THRESHOLD_ENERGY = threshold_energy
        self.frames = []

    def start_recording(self, duration=4):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS,
                            rate=self.RATE, input=True,
                            frames_per_buffer=self.CHUNK)
        print("Listening...")

        # Record for 'duration' seconds initially to disregard audio
        start_time = time.time()
        while time.time() - start_time < duration:
            print(time.time() - start_time)
            data = stream.read(self.CHUNK)
            self.frames.append(data)

        # Then continue recording and check for voice activity
        try:
            while True:
                data = stream.read(self.CHUNK)
                self.frames.append(data)
                samples = struct.unpack(f'{self.CHUNK}h', data)
                energy = np.sum(np.square(samples)) / self.CHUNK
                print(f'Energy: {energy}')
                if energy >= self.THRESHOLD_ENERGY:
                    print("Voice activity detected!")
                    break  # Exit the loop if voice activity detected
        except KeyboardInterrupt:
            pass
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()
            self.save_recording()

    def save_recording(self):
        folder_path = "/home/ito/amr_ws/mechine learing/project/mic/mic_data"
        file_name = str(len(os.listdir(folder_path))) + ".wav"
        file_path = os.path.join(folder_path, file_name)

        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(self.frames))
        print(f"Recorded audio saved at: {file_path}")

    def handle_interrupt(self, sig, frame):
        self.save_recording()
        exit(0)

if __name__ == "__main__":
    recorder = VoiceRecorder()
    signal.signal(signal.SIGINT, recorder.handle_interrupt)
    for i in range(1, 5):
        recorder.start_recording()
