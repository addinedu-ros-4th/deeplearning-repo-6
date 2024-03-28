import openai
from googleapi import AudioTranscriber, FileMonitor
import os
import json
import random
import threading
import time

class ChatGPTAssistant:
    def __init__(self, model_configs):
        self.model_configs = model_configs

        self.model_config_file_paths = [
            "/home/ito/amr_ws/mechine learing/project/mic/gpt/models/F.json",
            "/home/ito/amr_ws/mechine learing/project/mic/gpt/models/T.json",
            "/home/ito/amr_ws/mechine learing/project/mic/gpt/models/Default.json"
        ]

    def update_model_config(self, model_configs):
        self.model_configs = model_configs
        print("Model configurations updated")

        

    def get_messages(self, model_index):
        try:
            file_path = self.model_config_file_paths[model_index]
            with open(file_path, "r", encoding="utf-8") as f:
                messages = json.load(f)
            return messages
        except Exception as e:
            print("Failed to load messages for model {}: {}".format(model_index, str(e)))
            return None

    def chat_with_gpt(self, user_input_msg, model_index):
        try:
            OPENAI_YOUR_KEY = "api-key"
            openai.api_key = OPENAI_YOUR_KEY

            MAX_TOKENS = 150

            model_config = self.model_configs[model_index]

            response = openai.ChatCompletion.create(
                model=model_config["model"],
                messages=[
                    {"role": "system", "content": model_config["system_message"]},
                    {"role": "user", "content": user_input_msg}, 
                    {"role": "assistant", "content": model_config["assistant_message"]},
                ],
                temperature=0.,
                max_tokens=MAX_TOKENS
            )

            last_response = response["choices"][-1]["message"]["content"]
            return last_response
        except Exception as e:
            print("Exception in ChatGPTAssistant:", str(e))
            print("Error occurred in chat_with_gpt method.")

            return None

    def process_audio(self, file_path, model_key):
        print("Processing audio:", file_path)
        audio_transcriber = AudioTranscriber(file_path)
        transcript = audio_transcriber.transcribe_audio()
        if transcript is None:
            print("Failed to transcribe audio:", file_path)
            return

        print("Transcript:", transcript)

        messages = self.get_messages(model_key)
        if messages:
            random_message = random.choice(messages)
            query = random_message.get("query", "")
            response = random_message.get("response", "")
            print("Query:", query)
            print("Response:", response)
            last_response = self.chat_with_gpt(response, model_key)
            if last_response is None:
                print("Failed to generate GPT response for audio:", file_path)
                return

            print(last_response)
            # 파일 처리 후 해당 파일을 처리된 파일 리스트에서 삭제
            os.remove(file_path)

class ModelConfigThread(threading.Thread):
    def __init__(self, model_configs, assistant, interval=10):
        super(ModelConfigThread, self).__init__()
        self.model_configs = model_configs
        self.assistant = assistant
        self.interval = interval
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            time.sleep(self.interval)  # 일정 시간 간격으로만 실행하도록 수정
            self.assistant.update_model_config(self.model_configs)  # 모델 설정 업데이트
            print("Model configurations updated")

    def stop(self):
        self.stop_event.set()
