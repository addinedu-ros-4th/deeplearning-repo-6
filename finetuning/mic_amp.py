import os
import threading
from time import sleep
from pydub import AudioSegment

class AudioAmplifier:
    def __init__(self, directory, gain_dB):
        self.directory = directory
        self.gain_dB = gain_dB
        self.amplified_files = set()

    def amplify_audio(self, input_file, output_file):
        audio = AudioSegment.from_file(input_file)
        amplified_audio = audio + self.gain_dB
        amplified_audio.export(output_file, format=input_file.split('.')[-1])
        print(f"Amplified {input_file} and saved as {output_file}")
        self.amplified_files.add(output_file)

    def process_directory(self):
        while True:
            for filename in os.listdir(self.directory):
                if filename.endswith(".wav"):
                    input_file = os.path.join(self.directory, filename)
                    output_file = os.path.join(self.directory, filename)
                    if output_file not in self.amplified_files:
                        self.amplify_audio(input_file, output_file)
            sleep(1)
