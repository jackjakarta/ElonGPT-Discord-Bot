import openai
import discord
import requests
import time
import random
import string
import os
import urllib.parse

# Load the Discord Token from the .env file
TOKEN = os.environ['DISCORD_TOKEN']

# Load the OpenAI API Key from the .env file
openai.api_key = os.environ['OPENAI_API_KEY']

# Load the CoinMarketCap API Key from the .env file
API_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
API_KEY = os.environ['CMC_PRO_API_KEY']

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
    

    if message.content.startswith("?info"):
        guild_count = len(client.guilds)
        server_count = f"The bot is active on {guild_count} server(s)."
        embed = discord.Embed(title="bot activity", description=server_count, color=0x4BA081)
        await message.channel.send(embed=embed)


    if message.content.startswith("?fast"):
        chatinp = message.content[9:]
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
              {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."},
              {"role": "user", "content": f"{chatinp}"},
            ]
        )
        answer = response['choices'][0]['message']['content']
        #embed = discord.Embed(title="ChatGPT Response", description=answer, color=0x4BA081)
        await message.channel.send(answer) 


    if message.content.startswith("?ask"):
        gpt4inp = message.content[9:]
        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
              {"role": "system", "content": "You are ChatGPT, a large language model trained by OpenAI. Answer as concisely as possible."},
              {"role": "user", "content": f"{gpt4inp}"},
            ]
        )
        answer = response['choices'][0]['message']['content']
        #embed = discord.Embed(title="ChatGPT Response", description=answer, color=0x4BA081)
        await message.channel.send(answer) 


    if message.content.startswith("?gpt"):
        question = message.content[8:]
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            max_tokens=900,
            n = 1,
            stop=None,
            temperature=1,
        )
        await message.channel.send(response["choices"][0]["text"])     


    if message.content.startswith("?recipe"):
        ingredients = message.content[9:]
        prompt = f"Write a recipe based on these ingredients:\n\n{ingredients}"
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
              {"role": "system", "content": "You are ChefGPT, a master chef that provides the best recipes."},
              {"role": "user", "content": f"{prompt}"},
            ]
        )
        recipe = response['choices'][0]['message']['content']
        await message.channel.send(recipe)
    
   
    if message.content.startswith("?fact"):
        topic = message.content[5:]
        prompt = f"Tell me a fun fact about:\n\n{topic}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=250,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )  
        await message.channel.send(response["choices"][0]["text"])
    

    if message.content.startswith("?joke"):
        question = message.content[9:]
        response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
              {"role": "system", "content": "You are Bill Burr the stand up comedian and you tell very funny jokes."},
              {"role": "user", "content": "Tell me a smart and funny joke"},
            ],
        )
        answer = response['choices'][0]['message']['content']
        #embed = discord.Embed(title="ChatGPT Response", description=answer, color=0x4BA081)
        await message.channel.send(answer)   
    

    if message.content.startswith("?roll"):
        question = message.content[9:]
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
              {"role": "system", "content": "You are a dice roller. You only roll the one dice and respond with the result of the dice roll."},
              {"role": "user", "content": "Roll the dice"},
            ]
        )
        answer = response['choices'][0]['message']['content']
        #embed = discord.Embed(title="ChatGPT Response", description=answer, color=0x4BA081)
        await message.channel.send(answer)      

  
    if message.content.startswith("?help"):
        help_text = "?ask - insert a question and get an answer from Elon (gpt-4) \n"\
                    "?fast - insert a question and get an answer in fast mode (gpt-3.5) \n"\
                    "?image - generate an image based on a description \n"\
                    "?roll - roll the dice \n"\
                    "?price - insert cryptocurrency symbol to get price and market cap \n"\
                    "?poll - example: ?poll what color?/blue/red/yellow \n" \
                    "?help - list of all commands \n"
            
        embed = discord.Embed(title="list of commands:", description=help_text, color=0x4BA081)
        await message.channel.send(embed=embed)


    if message.content.startswith("?image"):
        # Get the text input
        text = message.content[6:]

        # Generate an image using the Dall-E model
        prompt=f"Generate an image based on the following description:\n\n{text}"
        response = openai.Image.create(
            model="image-alpha-001",
            prompt=prompt,
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
            print(f"Image saved at: {image_path}")
        else:
            print("Failed to retrieve the image.")        


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
            await message.channel.send(f"The price of {symbol} is ${price:.2f} and its market capitalization is ${market_cap:.2f}.")
        else:
            # Send an error message to the Discord channel
            await message.channel.send(f"Could not get price and market capitalization for {symbol}")   
     
            
    if message.content.startswith("?collect"):
        # Open the data.txt file in append mode
        with open("data.txt", "a") as file:
            # Write the message content to the file
            file.write(message.content[8:] + "\n")
        await message.channel.send("Your information has been saved.")
    elif message.content == "?showdata":
        # Open the data.txt file in read mode
        with open("data.txt", "r") as file:
            # Read the contents of the file
            data = file.read()
        await message.channel.send("Data:\n" + data)             


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


client.run(TOKEN)
