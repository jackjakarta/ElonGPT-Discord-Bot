from openai import OpenAI

from utils.settings import OPENAI_API_KEY


class ChatGPT:
    """ChatGPT Class"""

    def __init__(self, model="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model

        self.messages = [
            {
                "role": "system",
                "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as "
                           "possible."
            }
        ]
        self.prompt = None
        self.completion = None

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

    def set_system_message(self, system_prompt):
        self.messages = [{"role": "system", "content": system_prompt}]

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
