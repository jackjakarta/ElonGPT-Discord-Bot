import openai
import discord
import requests
import time
import random
import string
import os
import urllib.parse
from keys import OPENAI_API_KEY, DISCORD_TOKEN, CMC_PRO_API_KEY
from functions_module import save_data, load_data


# Replace with your own Discord bot token
TOKEN = DISCORD_TOKEN

# Replace with your own OpenAI API key
openai.api_key = OPENAI_API_KEY

# Replace with your own CMC API Key
API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
API_KEY = CMC_PRO_API_KEY

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    activity = discord.Activity(name="?help", type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    guild_count = len(client.guilds)
    print(f"{client.user} has connected to Discord!")
    print(f"{client.user} is active on {guild_count} server(s).")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # GPT 4
    if message.content.startswith("?ask"):
        try:
            gpt4_input = message.content[5:]
            json_data = load_data("fine_tune.json")
            response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."},
                {"role": "user", "content": gpt4_input},
                ]
            )
            answer = response['choices'][0]['message']['content']
            #embed = discord.Embed(title="ChatGPT Response", description=answer, color=0x4BA081)
            await message.channel.send(answer)
            json_data.append({"prompt": gpt4_input, "completion": answer})
            save_data("fine_tune.json", json_data)
            print("Prompt - Completion Pair saved to fine_tune.json file!")
        except Exception as e:
            embed = discord.Embed(title="Unknown Error:", description=e, color=0x4BA081)
            await message.channel.send(embed=embed)
            print(f"Unknown Error: {e}")

    # GPT 3.5 Turbo
    if message.content.startswith("?fast"):
        try:
            gpt3_input = message.content[6:]
            json_data = load_data("fine_tune.json")
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."},
                {"role": "user", "content": gpt3_input},
                ]
            )
            answer = response['choices'][0]['message']['content']
            #embed = discord.Embed(title="ChatGPT Response", description=answer, color=0x4BA081)
            await message.channel.send(answer)
            json_data.append({"prompt": gpt3_input, "completion": answer})
            save_data("fine_tune.json", json_data)
            print("Prompt - Completion Pair saved to fine_tune.json file!") 
        except Exception as e:
            embed = discord.Embed(title="Unknown Error:", description=e, color=0x4BA081)
            await message.channel.send(embed=embed)
            print(f"Unknown Error: {e}")

    # Image Generation with DALL-E
    if message.content.startswith("?image"):
        try:
            # Get the text input
            text = message.content[7:]

            # Generate an image using the Dall-E model
            img_prompt = text
            response = openai.Image.create(
                prompt=img_prompt,
                n=1,
                size="1024x1024"
            )
            
            # Get the URL of the generated image
            image_url = response['data'][0]['url']

            # Send the URL as a message in Discord
            await message.channel.send(image_url)

            # Save the image to a folder on disk
            image_response = requests.get(image_url, stream=True)
            if image_response.status_code == 200:
                image_extension = image_url.split(".")[-1].split("?")[0]
                random_string = ''.join(random.choices(string.ascii_letters, k=6))
                timestamp = int(time.time())
                image_filename = f"generated_image_{timestamp}_{random_string}.{image_extension}"
                image_path = os.path.join("image_folder", image_filename)

                with open(image_path, 'wb') as image_file:
                    for chunk in image_response.iter_content(8192):
                        image_file.write(chunk)
                print(f"Image for prompt: '{img_prompt}' saved at: {image_path}")
            else:
                print("Failed to retrieve the image.")
        except Exception as e:
            embed = discord.Embed(title="Unknown Error:", description=e, color=0x4BA081)
            await message.channel.send(embed=embed)
            print(f"Unknown Error: {e}")

    # Recipe Generator
    if message.content.startswith("?recipe"):
        try:
            ingredients = message.content[8:]
            recipe_prompt = f"Write a recipe based on these ingredients:\n\n{ingredients}"
            response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are ChefGPT, a master chef that provides the best recipes."},
                {"role": "user", "content": recipe_prompt},
                ]
            )
            recipe = response['choices'][0]['message']['content']
            await message.channel.send(recipe)
            with open("recipes.txt", "a") as file:
                # Write the message content to the file
                file.write(f"\n{recipe}\n")
                print("Recipe saved in recipes.txt file!")
        except Exception as e:
            embed = discord.Embed(title="Unknown Error:", description=e, color=0x4BA081)
            await message.channel.send(embed=embed)
            print(f"Unknown Error: {e}")

    # Crypto Price
    if message.content.startswith("?price"):
        # Split the message into parts
        parts = message.content.split(" ")
        # Extract the cryptocurrency symbol
        symbol = parts[1].upper()
        # Make the API request to CoinMarketCap
        params = {
            "symbol": symbol,
            "convert": "USD",
            "CMC_PRO_API_KEY": API_KEY
        }
        response = requests.get(API_URL, params=params)
        # Check if the API request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            # Extract the cryptocurrency price and market capitalization
            price = data["data"][symbol]["quote"]["USD"]["price"]
            market_cap = data["data"][symbol]["quote"]["USD"]["market_cap"]
            # Send the cryptocurrency price and market capitalization to the Discord channel
            rsp = f"**Price:** ${price:.2f}\n**Market Cap:** ${market_cap:.2f}"
            embed = discord.Embed(title=symbol, description=rsp, color=0x4BA081)
            await message.channel.send(embed=embed)
        else:
            # Send an error message to the Discord channel
            await message.channel.send(f"Could not get price and market capitalization for {symbol}")

    # Poll Command
    if message.content.startswith("?poll"):
        # Get the poll question and answer options
        poll_data = message.content[6:].split('/')
        question = poll_data[0].strip()
        options = [option.strip() for option in poll_data[1:]]
        # Create the poll message embed
        embed = discord.Embed(title=question, color=0x4BA081)
        for i, option in enumerate(options):
            embed.add_field(name=f"{i+1}. {option}", value="\u200b", inline=False)
        # Send the poll message and save it to a variable
        poll_message = await message.channel.send(embed=embed)
        # Add the reactions to the poll message
        for i in range(len(options)):
            await poll_message.add_reaction(f'{i+1}\u20e3')

    # Help Command
    if message.content.startswith("?help"):
        help_text = "?ask - insert a question and get an answer from Elon (gpt-4) \n"\
                    "?fast - insert a question and get an answer in fast mode (gpt-3.5) \n"\
                    "?image - generate an image based on a description \n"\
                    "?recipe - insert ingredients and get recipe \n"\
                    "?price - insert cryptocurrency symbol to get price and market cap \n"\
                    "?poll - example: ?poll what color?/blue/red/yellow \n" \
                    "?help - list of all commands \n"
            
        embed = discord.Embed(title="list of commands:", description=help_text, color=0x4BA081)
        await message.channel.send(embed=embed)


if __name__ == "__main__":
    client.run(TOKEN)
