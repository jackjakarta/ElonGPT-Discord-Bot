import os
import random
import string
import requests

from openai import OpenAI
from decouple import config
from utils import save_json, load_json, create_embed


# Constants and Configuration
OPENAI_API_KEY = config("OPENAI_API_KEY")
CMC_API_URL = config("CMC_API_URL")
CMC_API_KEY = config("CMC_PRO_API_KEY")
IMAGE_FOLDER = config("IMAGE_FOLDER")
RECIPES_FILE = config("RECIPES_FILE")
COMPLETIONS_FILE = config("COMPLETIONS_FILE")


async def ask_command(message):
    try:
        ai = OpenAI(api_key=OPENAI_API_KEY)
        prompt = message.content[5:]
        json_data = load_json(COMPLETIONS_FILE)
        response = ai.chat.completions.create(
            model="gpt-4-turbo-preview",
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
    except Exception as e:
        embed = create_embed(title="Unknown Error:", description=e)
        await message.channel.send(embed=embed)
        print(f"Unknown Error: {e}")


async def fast_command(message):
    try:
        ai = OpenAI(api_key=OPENAI_API_KEY)
        prompt = message.content[5:]
        json_data = load_json(COMPLETIONS_FILE)
        response = ai.chat.completions.create(
            model="gpt-3.5-turbo",
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
    except Exception as e:
        embed = create_embed(title="Unknown Error:", description=e)
        await message.channel.send(embed=embed)
        print(f"Unknown Error: {e}")


async def image_command(message):
    try:
        ai = OpenAI(api_key=OPENAI_API_KEY)
        prompt = message.content[7:]

        response = ai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

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
    except Exception as e:
        embed = create_embed(title="Unknown Error:", description=e)
        await message.channel.send(embed=embed)
        print(f"Unknown Error: {e}")


async def recipe_command(message):
    try:
        ai = OpenAI(api_key=OPENAI_API_KEY)
        ingredients = message.content[8:]
        recipe_prompt = f"Write a recipe based on these ingredients:\n\n{ingredients}"
        response = ai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are ChefGPT, a master chef that provides the best recipes."},
                {"role": "user", "content": recipe_prompt},
            ]
        )
        recipe = response.choices[0].message.content
        await message.channel.send(recipe)

        # Write the message content to a text file
        with open(RECIPES_FILE, "a") as file:
            file.write(f"\n{recipe}\n\n")
            print(f"Recipe saved in {RECIPES_FILE} file!")
    except Exception as e:
        embed = create_embed(title="Unknown Error:", description=e)
        await message.channel.send(embed=embed)
        print(f"Unknown Error: {e}")


async def price_command(message):
    # Split the message into parts
    parts = message.content.split(" ")
    # Extract the cryptocurrency symbol
    symbol = parts[1].upper()
    # Make the API request to CoinMarketCap
    params = {
        "symbol": symbol,
        "convert": "USD",
        "CMC_PRO_API_KEY": CMC_API_KEY
    }
    response = requests.get(CMC_API_URL, params=params)
    # Check if the API request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        # Extract the cryptocurrency price and market capitalization
        price = data["data"][symbol]["quote"]["USD"]["price"]
        market_cap = data["data"][symbol]["quote"]["USD"]["market_cap"]
        # Send the cryptocurrency price and market capitalization to the Discord channel
        rsp = f"**Price:** ${price:.2f}\n**Market Cap:** ${market_cap:.2f}"
        embed = create_embed(title=symbol, description=rsp)
        await message.channel.send(embed=embed)
    else:
        # Send an error message to the Discord channel
        await message.channel.send(f"Could not get price and market capitalization for {symbol}")


async def classify_command(message):
    try:
        input_url = message.content[10:]
        ai = OpenAI(api_key=OPENAI_API_KEY)

        response = ai.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What’s in this image? Answer in one paragraph maximum."},
                        {
                            "type": "image_url",
                            "image_url": input_url,
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        answer = response.choices[0].message.content
        await message.channel.send(answer)
    except Exception as e:
        embed = create_embed(title="Unknown Error:", description=e)
        await message.channel.send(embed=embed)
        print(f"Unknown Error: {e}")


async def poll_command(message):
    # Get the poll question and answer options
    poll_data = message.content[6:].split('/')
    question = poll_data[0].strip()
    options = [option.strip() for option in poll_data[1:]]
    # Create the poll message embed
    embed = create_embed(title=question, description=None)
    for i, option in enumerate(options):
        embed.add_field(name=f"{i + 1}. {option}", value="\u200b", inline=False)
    # Send the poll message and save it to a variable
    poll_message = await message.channel.send(embed=embed)
    # Add the reactions to the poll message
    for i in range(len(options)):
        await poll_message.add_reaction(f'{i + 1}\u20e3')


async def joke_command(message):
    try:
        joke_url = "https://api.chucknorris.io/jokes/random?category=science"
        api_response = requests.get(joke_url)
        joke = api_response.json()
        joke_format = joke["value"]

        await message.channel.send(joke_format)
    except Exception as e:
        embed = create_embed(title="API Call Error:", description=e)
        await message.channel.send(embed=embed)
        print(f"API Call Error: {e}")


async def help_command(message):
    help_text = "?ask - insert a question and get an answer from Elon (gpt-4) \n" \
                "?fast - insert a question and get an answer in fast mode (gpt-3.5) \n" \
                "?image - generate an image based on a description \n" \
                "?classify - classify an image based on an url \n" \
                "?recipe - insert ingredients and get recipe \n" \
                "?price - insert cryptocurrency symbol to get price and market cap \n" \
                "?poll - example: ?poll what color?/blue/red/yellow \n" \
                "?help - list of all commands \n"

    embed = create_embed(title="list of commands:", description=help_text)
    await message.channel.send(embed=embed)
