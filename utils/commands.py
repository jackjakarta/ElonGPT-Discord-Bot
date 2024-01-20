import os
import random
import string
import requests

from openai import OpenAI
from decouple import config
from utils.utils import save_json, load_json, create_embed


# Constants and Configuration
DISCORD_TOKEN = config("DISCORD_TOKEN")
OPENAI_API_KEY = config("OPENAI_API_KEY")
CMC_API_URL = config("CMC_API_URL")
CMC_API_KEY = config("CMC_PRO_API_KEY")
EVNTMNGR_API_URL = config("EVNTMNGR_API_URL")
EVNTMNGR_API_KEY = config("EVNTMNGR_API_KEY")
IMAGE_FOLDER = config("IMAGE_FOLDER")
RECIPES_FILE = config("RECIPES_FILE")
COMPLETIONS_FILE = config("COMPLETIONS_FILE")


async def ask_command(message):
    ai = OpenAI(api_key=OPENAI_API_KEY)
    prompt = message.content[5:]
    json_data = load_json(COMPLETIONS_FILE)
    response = ai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI."
                                          "Answer as concisely as possible."},
            {"role": "user", "content": prompt},
        ]
    )
    answer = response.choices[0].message.content
    await message.channel.send(answer)
    json_data.append({"prompt": prompt, "completion": answer})
    save_json(COMPLETIONS_FILE, json_data)
    print("Prompt - Completion Pair saved to completions.json file!")


async def fast_command(message):
    # Implementation for ?fast command
    pass  # Similar to existing implementation


async def image_command(message):
    ai = OpenAI(api_key=OPENAI_API_KEY)
    prompt = message.content[7:]

    response = ai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    # Img URL
    image_url = response.data[0].url

    await message.channel.send(image_url)

    # Save Image
    img_response = requests.get(image_url, stream=True)
    if img_response.status_code == 200:
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        image_folder = IMAGE_FOLDER
        image_filename = f"image_{random_string}.png"
        os.makedirs(image_folder, exist_ok=True)
        image_path = os.path.join(image_folder, image_filename)

        with open(image_path, "wb") as image_file:
            for chunk in img_response.iter_content(8192):
                image_file.write(chunk)
        print(f"Image for prompt: '{prompt}' saved at: {image_path}.")
    else:
        print("Failed to saved image!")


async def recipe_command(message):
    # Implementation for ?recipe command
    pass  # Similar to existing implementation


async def price_command(message):
    # Implementation for ?price command
    pass  # Similar to existing implementation


async def poll_command(message):
    pass


async def joke_command(message):
    # Implementation for ?joke command
    pass  # Similar to existing implementation


async def help_command(message):
    # Implementation for ?help command
    pass  # Similar to existing implementation
