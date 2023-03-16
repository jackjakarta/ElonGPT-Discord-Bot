import openai
import discord
import os
import requests

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
    activity = discord.Activity(name='use | ?help', type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("?ask"):
        question = message.content[9:]
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
              #{"role": "system", "content": "You are a helpful assistant."},
              {"role": "user", "content": f"{question}"},
            ]
        )
        answer = response['choices'][0]['message']['content']
        #embed = discord.Embed(title="ChatGPT Response", description=answer, color=0x4BA081)
        await message.channel.send(answer) 

    
    if message.content.startswith("?gpt3"):
        question = message.content[5:]
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=(f"{question}"),
            max_tokens=900,
            n = 1,
            stop=None,
            temperature=1,
        )
        await message.channel.send(response["choices"][0]["text"])


    if message.content.startswith("?recipe"):
        ingredients = message.content[8:]
        prompt = f"Write a recipe based on these ingredients:\n\n{ingredients}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.5,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )  
        await message.channel.send(response["choices"][0]["text"])
    
  
    if message.content.startswith("?fact"):
        topic = message.content[4:]
        prompt = f"Tell me a fun fact about:\n\n{topic}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
            max_tokens=250,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )  
        await message.channel.send(response["choices"][0]["text"])

        
    if message.content.startswith("?keypoints"):
        subject = message.content[4:]
        prompt = f"Highlight 5 keypoints about:\n\n{subject}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.6,
            max_tokens=550,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )  
        await message.channel.send(response["choices"][0]["text"])   

        
    if message.content.startswith("?study"):
        studytopic = message.content[4:]
        prompt = f"What are 5 key points I should know when studying:\n\n{studytopic}"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.4,
            max_tokens=600,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )  
        await message.channel.send(response["choices"][0]["text"])  


    if message.content.startswith("?joke"):
        prompt = "Tell me a joke"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=1,
            max_tokens=400,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )  
        await message.channel.send(response["choices"][0]["text"])

  
    if message.content.startswith("?roll"):
        prompt = "Roll the dice"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=1,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )  
        await message.channel.send(response["choices"][0]["text"])
  
  
    if message.content.startswith("?help"):
        help_text = "?ask - insert a question and get an answer using the new gpt-3.5-turbo model \n" \
                    "?gpt3 - insert a question and get an answer using the text-davinci-003 model \n"\
                    "?recipe - insert ingredients separeted by commas and get a recipe \n"\
                    "?fact - insert a topic and get a fun fact \n"\
                    "?keypoints - insert a topic to highlight 5 keypoints about that topic \n"\
                    "?study - insert a topic and get study notes \n"\
                    "?image - generate image based on a description \n"\
                    "?joke - tell me a joke \n"\
                    "?roll - roll the dice \n"\
                    "?price - insert cryptocurrency symbol to get price and market cap \n"\
                    "?collect - collects inserted text and stores it in a document on the server \n"\
                    "?showdata - shows the contets of the document mentioned previously \n"\
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


client.run(TOKEN)

