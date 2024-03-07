import os

from openai import OpenAI

from utils import load_json_chat, save_json
from utils.settings import OPENAI_API_KEY, CHATS_FOLDER


class ChatGPT:
    """ChatGPT Class"""

    def __init__(self, user_name=None, model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model
        self.prompt = None
        self.completion = None

        self.chats_dir = CHATS_FOLDER
        self.chat_file = f"chat_{user_name}.json"

        self.messages = load_json_chat(os.path.join(self.chats_dir, self.chat_file))

    def ask(self, prompt):
        self.prompt = prompt

        if self.prompt:
            self.messages.append(
                {"role": "user", "content": self.prompt}
            )

        self.completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=400
        )
        self.messages.append({"role": "assistant", "content": str(self.completion.choices[0].message.content)})

        return self.completion.choices[0].message.content

    def save_chat(self):
        json_data = self.messages
        file_path = os.path.join(self.chats_dir, self.chat_file)
        save_json(file_path, json_data)

    def reset_chat(self):
        self.messages.append(
            {
                "role": "user",
                "content": "Clear the chat and start a new session. Forget everything we talked about before."
            }
        )

    def set_system_message(self, system_prompt):
        self.messages.append({"role": "system", "content": system_prompt})

    def get_models(self):
        models_list = self.client.models.list().data
        models = [x.id for x in models_list]

        return sorted(models)


class ImageClassify(ChatGPT):
    def __init__(self, model="gpt-4-vision-preview"):
        super().__init__(model)
        self.messages = [
            {
                "role": "system",
                "content": "You are an AI Vision model. Classify the images in one paragraph."
            }
        ]
        self.image_url = None

    def interpret_image_url(self, image_url: str, prompt: str = "Classify this image."):
        self.image_url = image_url
        self.prompt = prompt

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

        self.completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            max_tokens=650
        )
        self.messages.append({"role": "assistant", "content": str(self.completion.choices[0].message.content)})

        return self.completion.choices[0].message.content
