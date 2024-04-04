import json
import openai

# OpenAI API 키 설정
# openai.api_key = api_key

class ChatGPTAssistant:
    def __init__(self, model_configs):
        self.model_configs = model_configs
        self.models = {}

    def train_models(self):
        for model_name, config in self.model_configs.items():
            print(f"Training model: {model_name}")
            # 대화 데이터 로드 및 학습
            with open(config['file_path'], 'r', encoding='utf-8') as file:
                conversation_data = json.load(file)
            
            # 대화 데이터 변환
            converted_conversation = []
            for item in conversation_data:
                converted_conversation.append({
                    "role": "system",
                    "content": item["query"]
                })
                converted_conversation.append({
                    "role": "user",
                    "content": item["response"]
                })
            
            # 모델 학습
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # 적절한 엔진 선택
                messages=converted_conversation,
                temperature=0.7,
                max_tokens=100,
                stop=None
            )
            
            # 학습된 모델 저장
            self.models[model_name] = response

    def save_models(self, output_dir):
        for model_name, model_data in self.models.items():
            output_file = f"{output_dir}/{model_name}.json"
            with open(output_file, 'w', encoding='utf-8') as file:
                json.dump(model_data, file)

def main():
    # 모델 설정 파일 경로
    model_configs = {
        'T': {'file_path': 'train_models/T.json'},  # T.json 파일 경로
        'F': {'file_path': 'train_models/F.json'},  # F.json 파일 경로
        'Default': {'file_path': 'train_models/Thanos.json'}  # Thanos.json 파일 경로
    }

    # ChatGPTAssistant 인스턴스 생성
    assistant = ChatGPTAssistant(model_configs)

    # 모델 학습
    assistant.train_models()

    # 학습된 모델을 파일로 저장
    assistant.save_models(output_dir="")

if __name__ == "__main__":
    main()
