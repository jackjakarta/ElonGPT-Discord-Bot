import json
import random
import string
import time
from datetime import datetime, timezone, timedelta

from discord import Embed
from openai import OpenAI

from .settings import OPENAI_API_KEY


def load_json(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        with open(filename, 'w') as file:
            json.dump([], file)
        return []


def load_json_chat(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError:
        with open(filename, 'w') as file:
            messages = [
                {
                    "role": "system",
                    "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as "
                               "possible."
                }
            ]
            json.dump(messages, file)
        return []


def save_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


def create_embed(title, description, color=0xFFFFFF):
    """Create a Discord embed."""
    return Embed(title=title, description=description, color=color)


def check_moderate(input_text: str) -> bool:
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.moderations.create(input=input_text, model="text-moderation-stable")
    categories_object = response.results[0].categories

    if any(getattr(categories_object, attr) for attr in categories_object.__dict__):
        return True
    else:
        return False


class RandomGenerator:
    """Random String Generator. Default length is 10 characters."""
    def __init__(self):
        self.length = None

    def random_string(self, length=6):
        self.length = length

        characters = string.ascii_lowercase + string.digits
        random_generate = "".join(random.choices(characters, k=self.length))

        return random_generate

    def random_digits(self, length=6):
        self.length = length

        characters = string.digits
        random_generate = "".join(random.choices(characters, k=self.length))

        return random_generate

    def random_letters(self, length=6):
        self.length = length

        characters = string.ascii_letters
        random_generate = "".join(random.choices(characters, k=self.length))

        return random_generate

    @staticmethod
    def timestamp(tz_delta: int = 1):
        timestamp = time.time()
        time_zone = timezone(timedelta(tz_delta))
        datetime_obj = datetime.fromtimestamp(timestamp, tz=time_zone)
        formatted_date = datetime_obj.strftime('%d-%m-%Y')
        formatted_time = datetime_obj.strftime('%H-%M')

        timestamp_formatted = f"{formatted_date}_{formatted_time}"

        return timestamp_formatted
