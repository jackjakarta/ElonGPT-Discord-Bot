import os

from openai import OpenAI
from ollama import Client
from utils import load_json_chat, save_json
from utils.settings import OPENAI_API_KEY, CHATS_FOLDER, OLLAMA_SERVER


class ChatGPT:
    """ChatGPT Class"""

    def __init__(self, user_name=None, model="gpt-4-turbo"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model
        self.prompt = None
        self.completion = None

        self.chats_dir = CHATS_FOLDER
        self.chat_file = f"chat_{user_name}.json"

        self.messages = load_json_chat(os.path.join(self.chats_dir, self.chat_file))

    def ask(self, prompt, max_tokens: int = 400):
        self.prompt = prompt

        if self.prompt:
            self.messages.append(
                {"role": "user", "content": self.prompt}
            )

        self.completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=max_tokens
        )
        self.messages.append({"role": "assistant", "content": str(self.completion.choices[0].message.content)})

        return self.completion.choices[0].message.content

    def save_chat(self):
        json_data = self.messages
        file_path = os.path.join(self.chats_dir, self.chat_file)
        save_json(file_path, json_data)

    def delete_chat(self):
        os.remove(os.path.join(self.chats_dir, self.chat_file))
        self.messages.append(
            {
                "role": "system",
                "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as "
                           "possible."
            }
        )

    def get_models(self):
        models_list = self.client.models.list().data
        models = [x.id for x in models_list]

        return sorted(models)


class ImageClassify(ChatGPT):
    def __init__(self, prompt="Classify this image."):
        super().__init__()
        self.messages = []
        self.image_url = None
        self.prompt = prompt

    def classify_image(self, image_url: str):
        self.image_url = image_url
        self.messages = []  # Clearing messages for each new classification

        msg_dict = {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": self.prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": self.image_url,
                    },
                },
            ],
        }

        if self.image_url:
            self.messages.append(msg_dict)

        try:
            self.completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                max_tokens=650
            )
            assistant_response = self.completion.choices[0].message.content
        except Exception as e:
            assistant_response = f"Error: {str(e)}"

        return assistant_response


class Ollama:
    """Ollama Class"""

    def __init__(self, model="orca-mini"):
        self.client = Client(host=OLLAMA_SERVER)
        self.model = model
        self.prompt = None
        self.completion = None
        self.messages = []

    def ask(self, prompt):
        self.prompt = prompt

        if self.prompt:
            self.messages.append(
                {"role": "user", "content": self.prompt}
            )

        self.completion = self.client.chat(model=self.model, messages=self.messages)
        response = self.completion.get('message').get('content')

        self.messages.append({"role": "assistant", "content": response})

        return response
