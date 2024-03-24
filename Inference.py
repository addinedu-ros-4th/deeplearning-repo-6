# Copyright (c) 2020, Soohwan Kim. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
sys.path.append("/Users/djy/Desktop/project/kospeech_latest")


import torch
import torch.nn as nn
import numpy as np
import torchaudio
from torch import Tensor
from kospeech_latest.kospeech.vocabs.ksponspeech import KsponSpeechVocabulary
from kospeech_latest.kospeech.data.audio.core import load_audio
from kospeech_latest.kospeech.models import (
    SpeechTransformer,
    Jasper,
    DeepSpeech2,
    ListenAttendSpell,
    Conformer,
)

class Inference:
    def __init__(self) -> None:
        self.model_path =  '/Users/djy/Desktop/project/model_ds2.pt'
        self.audio_path = '/Users/djy/Desktop/project/0.wav'
        self.device = 'cpu'

    def parse_audio(self, audio_path: str, del_silence: bool = False, audio_extension: str = 'pcm') -> Tensor:
        signal = load_audio(audio_path, del_silence, extension=audio_extension)
        feature = torchaudio.compliance.kaldi.fbank(
            waveform=Tensor(signal).unsqueeze(0),
            num_mel_bins=80,
            frame_length=20,
            frame_shift=10,
            window_type='hamming'
        ).transpose(0, 1).numpy()

        feature -= feature.mean()
        feature /= np.std(feature)

        return torch.FloatTensor(feature).transpose(0, 1)

    def inference(self):
        feature = self.parse_audio(self.audio_path, del_silence=True)
        input_length = torch.LongTensor([len(feature)])
        vocab = KsponSpeechVocabulary('/Users/djy/Desktop/project/kospeech_latest/data/vocab/aihub_character_vocabs.csv')

        model = torch.load(self.model_path, map_location=lambda storage, loc: storage).to(self.device)
        if isinstance(model, nn.DataParallel):
            model = model.module
        model.eval()

        if isinstance(model, ListenAttendSpell):
            model.encoder.device = self.device
            model.decoder.device = self.device
            y_hats = model.recognize(feature.unsqueeze(0), input_length)
        elif isinstance(model, DeepSpeech2):
            model.device = self.device
            y_hats = model.recognize(feature.unsqueeze(0), input_length)
        elif isinstance(model, SpeechTransformer) or isinstance(model, Jasper) or isinstance(model, Conformer):
            y_hats = model.recognize(feature.unsqueeze(0), input_length)

        sentence = vocab.label_to_string(y_hats.cpu().detach().numpy())
        print(sentence)

    
if __name__ == "__main__":
    model_path = '/Users/djy/Desktop/project/model_ds2.pt'
    audio_path = '/Users/djy/Desktop/project/3.wav'
    device = 'cpu'

    def parse_audio(audio_path: str, del_silence: bool = False, audio_extension: str = 'pcm') -> Tensor:
        signal = load_audio(audio_path, del_silence, extension=audio_extension)
        feature = torchaudio.compliance.kaldi.fbank(
            waveform=Tensor(signal).unsqueeze(0),
            num_mel_bins=80,
            frame_length=20,
            frame_shift=10,
            window_type='hamming'
        ).transpose(0, 1).numpy()

        feature -= feature.mean()
        feature /= np.std(feature)

        return torch.FloatTensor(feature).transpose(0, 1)


    feature = parse_audio(audio_path, del_silence=True)
    input_length = torch.LongTensor([len(feature)])
    vocab = KsponSpeechVocabulary('/Users/djy/Desktop/project/kospeech_latest/data/vocab/aihub_character_vocabs.csv')

    model = torch.load(model_path, map_location=lambda storage, loc: storage).to(device)
    if isinstance(model, nn.DataParallel):
        model = model.module
    model.eval()

    if isinstance(model, ListenAttendSpell):
        model.encoder.device = device
        model.decoder.device = device
        y_hats = model.recognize(feature.unsqueeze(0), input_length)
    elif isinstance(model, DeepSpeech2):
        model.device = device
        y_hats = model.recognize(feature.unsqueeze(0), input_length)
    elif isinstance(model, SpeechTransformer) or isinstance(model, Jasper) or isinstance(model, Conformer):
        y_hats = model.recognize(feature.unsqueeze(0), input_length)

    sentence = vocab.label_to_string(y_hats.cpu().detach().numpy())
    print(sentence)
