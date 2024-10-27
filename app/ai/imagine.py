import os

import requests
from openai import OpenAI

from utils import RandomGenerator
from utils.settings import IMAGE_FOLDER, OPENAI_API_KEY


class ImageDallE:
    """Image Generation with the OpenAI DALL-E model."""

    def __init__(self, model="dall-e-3", image_folder=IMAGE_FOLDER):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model
        self.image_folder = image_folder
        self.prompt = None
        self.response = None
        self.image_url = None
        self.image_path = None

    def generate_image(self, prompt):
        self.prompt = prompt
        self.response = self.client.images.generate(
            model=self.model,
            prompt=self.prompt,
            size="1792x1024",
            quality="hd",
            n=1,
        )
        self.image_url = self.response.data[0].url

        return self.image_url

    def save_image(self, image_name=RandomGenerator().random_string()):
        request_response = requests.get(self.image_url, stream=True)

        if request_response.status_code == 200:
            image_filename = f"image_{image_name}.png"
            self.image_path = os.path.join(self.image_folder, image_filename)

            with open(self.image_path, "wb+") as f:
                for chunk in request_response.iter_content(8192):
                    f.write(chunk)
            return f"\nImaged saved at: {self.image_path}."
        else:
            return "\nFailed to get image!"

    def delete_image(self, image_name):
        image_filename = f"image_{image_name}.png"
        os.remove(os.path.join(self.image_folder, image_filename))
        print("\nImage deleted successfully.")
